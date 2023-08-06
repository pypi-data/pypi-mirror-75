#!/usr/bin/env python3

"""
Will use the PyCharm code inspection.

See here:
  https://github.com/albertz/pycharm-inspect
  https://stackoverflow.com/questions/55323910/pycharm-code-style-check-via-command-line
  https://youtrack.jetbrains.com/issue/PY-34864
"""

import os
import sys
import subprocess
import tempfile
from glob import glob
import argparse

my_dir = os.path.dirname(os.path.abspath(__file__))
base_dir = os.path.dirname(my_dir)
sys.path.insert(0, base_dir)
os.chdir(base_dir)

from returnn.util import better_exchook  # noqa
better_exchook.install()


def check_pycharm_dir(pycharm_dir):
  """
  :param str pycharm_dir:
  """
  assert os.path.isdir(pycharm_dir)
  assert os.path.exists("%s/bin/inspect.sh" % pycharm_dir)


def install_pycharm():
  """
  :return: pycharm dir
  :rtype: str
  """
  # travis_fold: https://github.com/travis-ci/travis-ci/issues/1065
  print("travis_fold:start:script.install")
  print("Install PyCharm...")
  pycharm_dir = "%s/pycharm" % tempfile.mkdtemp()
  subprocess.check_call([my_dir + "/install_pycharm.sh"], cwd=os.path.dirname(pycharm_dir), stderr=subprocess.STDOUT)
  check_pycharm_dir(pycharm_dir)
  print("travis_fold:end:script.install")
  return pycharm_dir


def get_version_str_from_pycharm(pycharm_dir):
  """
  :param str pycharm_dir:
  :return: e.g. "CE2018.3"
  :rtype: str
  """
  import re
  code = open("%s/bin/pycharm.sh" % pycharm_dir).read()
  m = re.search("-Didea\\.paths\\.selector=PyCharm(\\S+) ", code)
  return m.group(1)


def create_stub_dir(pycharm_dir, stub_dir):
  """
  :param str pycharm_dir:
  :param str stub_dir:
  """
  print("travis_fold:start:script.create_python_stubs")
  print("Generating Python stubs via helpers/generator3.py...")
  subprocess.check_call([sys.executable, "%s/helpers/generator3.py" % pycharm_dir, "-d", stub_dir, "-b"])
  print("Collecting further native modules...")
  for line in subprocess.check_output([
        sys.executable, "%s/helpers/generator3.py" % pycharm_dir, "-L"]).decode("utf8").splitlines()[1:]:
    # First line is version, so we skipped those.
    # Then we get sth like "<module name> <other things>...".
    assert isinstance(line, str)
    mod_name = line.split()[0]
    # Ignore errors here.
    subprocess.call([sys.executable, "%s/helpers/generator3.py" % pycharm_dir, "-d", stub_dir, mod_name])
  print("travis_fold:end:script.create_python_stubs")


_use_stub_zip = False


def setup_pycharm_python_interpreter(pycharm_dir):
  """
  Unfortunately, the headless PyCharm bin/inspect will use the global PyCharm settings,
  and requires that we have a Python interpreter set up,
  with the same name as we use in our `.idea` settings, which we will link in :func:`prepare_src_dir`.
  See here: https://youtrack.jetbrains.com/issue/PY-34864

  Our current way to work around this: We create (or extend) the file
  ``~/.PyCharm<VERSION>/config/options/jdk.table.xml`` such that it has the right Python interpreter.

  :param str pycharm_dir:
  """
  print("travis_fold:start:script.setup_pycharm_python_interpreter")
  name = "Python 3 (.../bin/python3)"  # used in our PyCharm.idea. this should match.
  pycharm_version = get_version_str_from_pycharm(pycharm_dir)  # should match in install_pycharm.sh
  if sys.platform == "darwin":
    pycharm_config_dir = os.path.expanduser("~/Library/Preferences/PyCharm%s" % pycharm_version)
    pycharm_system_dir = os.path.expanduser("~/Library/Caches/PyCharm%s" % pycharm_version)
  else:  # assume Linux/Unix
    pycharm_config_dir = os.path.expanduser("~/.PyCharm%s/config" % pycharm_version)
    pycharm_system_dir = os.path.expanduser("~/.PyCharm%s/system" % pycharm_version)

  # I just zipped the stubs from my current installation on Linux.
  # Maybe we can also reuse these stubs for other PyCharm versions, or even other Python versions.
  if _use_stub_zip:
    stub_base_name = "pycharm2018.3-python3.6-stubs"
    stub_fn = "%s/python_stubs/%s.zip" % (pycharm_system_dir, stub_base_name)
    stub_dir = "%s/python_stubs/%s" % (pycharm_system_dir, stub_base_name)
    os.makedirs(os.path.dirname(stub_fn), exist_ok=True)
    if os.path.exists(stub_dir):
      print("Python stubs dir exists already:", stub_dir)
    else:
      if not os.path.exists(stub_fn):
        subprocess.check_call([
          "wget",
          "https://www-i6.informatik.rwth-aachen.de/web/Software/returnn/%s.zip" % stub_base_name],
          cwd=os.path.dirname(stub_fn))
      assert os.path.exists(stub_fn)
      subprocess.check_call(
        ["unzip", "%s.zip" % stub_base_name, "-d", stub_base_name],
        cwd=os.path.dirname(stub_fn))
      assert os.path.isdir(stub_dir)
  else:
    stub_dir = "%s/python_stubs/python%s-generated" % (
      pycharm_system_dir, "%i.%i.%i" % sys.version_info[:3])
    print("Generate stub dir:", stub_dir)
    os.makedirs(stub_dir, exist_ok=True)
    create_stub_dir(pycharm_dir=pycharm_dir, stub_dir=stub_dir)

  jdk_table_fn = "%s/options/jdk.table.xml" % pycharm_config_dir
  print("Filename:", jdk_table_fn)
  os.makedirs(os.path.dirname(jdk_table_fn), exist_ok=True)

  import xml.etree.ElementTree as ElementTree
  if os.path.exists(jdk_table_fn):
    print("Loading existing jdk.table.xml.")
    et = ElementTree.parse(jdk_table_fn)
    root = et.getroot()
    assert isinstance(root, ElementTree.Element)
    jdk_collection = root.find("./component")
    assert isinstance(jdk_collection, ElementTree.Element)
    assert jdk_collection.tag == "component" and jdk_collection.attrib["name"] == "ProjectJdkTable"
  else:
    print("Creating new jdk.table.xml.")
    root = ElementTree.Element("application")
    et = ElementTree.ElementTree(root)
    jdk_collection = ElementTree.SubElement(root, "component", name="ProjectJdkTable")
    assert isinstance(jdk_collection, ElementTree.Element)

  existing_jdk = jdk_collection.find("./jdk/name[@value='%s']/.." % name)
  if existing_jdk:
    print("Found existing Python interpreter %r. Remove and recreate." % name)
    assert isinstance(existing_jdk, ElementTree.Element)
    assert existing_jdk.find("./name").attrib["value"] == name
    jdk_collection.remove(existing_jdk)

  # Example content:
  """
  <application>
  <component name="ProjectJdkTable">
    <jdk version="2">
      <name value="Python 2.7.3 (/usr/bin/python2.7)" />
      <type value="Python SDK" />
      <version value="Python 2.7.12" />
      <homePath value="/usr/bin/python2.7" />
      <roots>
        <classPath>
          <root type="composite">
            <root url="file:///usr/bin" type="simple" />
            ...
          </root>
        </classPath>
        <sourcePath>
          <root type="composite" />
        </sourcePath>
      </roots>
      <additional />
    </jdk>
  </component>
  </application>
  """

  jdk_entry = ElementTree.SubElement(jdk_collection, "jdk", version="2")
  ElementTree.SubElement(jdk_entry, "name", value=name)
  ElementTree.SubElement(jdk_entry, "type", value="Python SDK")
  ElementTree.SubElement(jdk_entry, "version", value="Python %i.%i.%i" % sys.version_info[:3])
  ElementTree.SubElement(jdk_entry, "homePath", value=sys.executable)
  paths_root = ElementTree.SubElement(jdk_entry, "roots")
  classes_paths = ElementTree.SubElement(ElementTree.SubElement(paths_root, "classPath"), "root", type="composite")
  relevant_paths = list(sys.path)
  if os.getcwd() in relevant_paths:
    relevant_paths.remove(os.getcwd())
  relevant_paths.extend([
    stub_dir,
    "$APPLICATION_HOME_DIR$/helpers/python-skeletons",
    "$APPLICATION_HOME_DIR$/helpers/typeshed/stdlib/3",
    "$APPLICATION_HOME_DIR$/helpers/typeshed/stdlib/2and3",
    "$APPLICATION_HOME_DIR$/helpers/typeshed/third_party/3",
    "$APPLICATION_HOME_DIR$/helpers/typeshed/third_party/2and3"
  ])
  # Maybe also add Python stubs path? How to generate them?
  for path in relevant_paths:
    ElementTree.SubElement(classes_paths, "root", url="file://%s" % path, type="simple")
  ElementTree.SubElement(ElementTree.SubElement(paths_root, "sourcePath"), "root", type="composite")
  ElementTree.SubElement(jdk_entry, "additional")

  print("Save XML.")
  et.write(jdk_table_fn, encoding="UTF-8")
  print("travis_fold:end:script.setup_pycharm_python_interpreter")


def prepare_src_dir(files=None):
  """
  New clean source dir, where we symlink only the relevant src files.

  :param list[str]|None files:
  :return: src dir
  :rtype: str
  """
  print("travis_fold:start:script.prepare")
  print("Prepare project source files...")
  if not files:
    files = ["returnn", "tools", "demos", "rnn.py", "setup.py", "__init__.py"]
  src_tmp_dir = "%s/returnn" % tempfile.mkdtemp()
  os.mkdir(src_tmp_dir)
  os.symlink("%s/PyCharm.idea" % my_dir, "%s/.idea" % src_tmp_dir)
  for fn in files:
    os.symlink(fn, "%s/%s" % (src_tmp_dir, os.path.basename(fn)))
  print("All source files:")
  subprocess.check_call(["ls", "-la", src_tmp_dir])
  print("travis_fold:end:script.prepare")
  return src_tmp_dir


def run_inspect(pycharm_dir, src_dir):
  """
  :param str pycharm_dir:
  :param str src_dir:
  :return: dir of xml files
  :rtype: str
  """
  out_tmp_dir = tempfile.mkdtemp()

  print("travis_fold:start:script.inspect")
  # Note: Will not run if PyCharm is already running.
  # Maybe we can find some workaround for this?
  # See here: https://stackoverflow.com/questions/55339010/run-pycharm-inspect-sh-even-if-pycharm-is-already-running
  # And here: https://github.com/albertz/pycharm-inspect
  # Also: https://stackoverflow.com/questions/55323910/pycharm-code-style-check-via-command-line
  cmd = [
    "%s/bin/inspect.sh" % pycharm_dir,
    src_dir,
    "%s/PyCharm-inspection-profile.xml" % my_dir,
    out_tmp_dir,
    "-v2"]
  print("$ %s" % " ".join(cmd))
  subprocess.check_call(cmd, stderr=subprocess.STDOUT)
  print("travis_fold:end:script.inspect")

  return out_tmp_dir


def report_inspect_xml(fn):
  """
  :param str fn:
  :return: list of (filename, line, problem_severity, inspect_class, description)
  :rtype: list[(str,int,str,str,str)]
  """
  # Example PyPackageRequirementsInspection.xml:
  """
  <problems is_local_tool="true">
  <problem>
    <file>file://$PROJECT_DIR$/TFUtil.py</file>
    <line>1</line>
    <module>returnn</module>
    <entry_point TYPE="file" FQNAME="file://$PROJECT_DIR$/TFUtil.py" />
    <problem_class severity="WARNING" attribute_key="WARNING_ATTRIBUTES">Package requirements</problem_class>
    <description>Package requirements 'h5py', 'theano==0.9' are not satisfied</description>
  </problem>
  </problems>
  """
  inspect_class = os.path.splitext(os.path.basename(fn))[0]  # e.g. "PyPackageRequirementsInspection"
  import xml.etree.ElementTree as ElementTree
  root = ElementTree.parse(fn).getroot()
  assert isinstance(root, ElementTree.Element)
  assert root.tag == "problems"
  result = []
  for problem in root.findall("./problem"):
    assert isinstance(problem, ElementTree.Element)
    assert problem.tag == "problem"
    filename = problem.find("./file").text.strip()
    if filename.startswith("file://$PROJECT_DIR$/"):
      filename = filename[len("file://$PROJECT_DIR$/"):]
    line = int(problem.find("./line").text.strip())
    problem_severity = problem.find("./problem_class").attrib["severity"]
    description = problem.find("./description").text.strip()
    result.append((filename, line, problem_severity, inspect_class, description))
  return result


def report_inspect_dir(path,
                       inspect_class_blacklist=None, inspect_class_not_counted=None,
                       ignore_count_for_files=()):
  """
  :param str path:
  :param set[str]|None inspect_class_blacklist:
  :param set[str]|None inspect_class_not_counted:
  :param set[str]|tuple[str]|None ignore_count_for_files:
  :return: count of reports
  :rtype: int
  """
  if os.path.isfile(path):
    assert path.endswith(".xml")
    fs = [path]
  else:
    assert os.path.isdir(path)
    fs = list(glob(path + "/*.xml"))
    assert fs

  inspections = []
  for fn in fs:
    inspections.extend(report_inspect_xml(fn))
  inspections.sort()
  inspections.append((None, None, None, None, None))  # final marker

  # copy
  inspect_class_blacklist = set(inspect_class_blacklist or ())
  inspect_class_not_counted = set(inspect_class_not_counted or ())

  # maybe update inspect_class_not_counted
  all_files = set()
  relevant_inspections_for_file = set()
  for filename, line, problem_severity, inspect_class, description in inspections:
    all_files.add(filename)
    if inspect_class in inspect_class_blacklist:
      continue
    if inspect_class in inspect_class_not_counted:
      continue
    relevant_inspections_for_file.add(filename)
  for filename in all_files:
    if filename not in relevant_inspections_for_file:
      ignore_count_for_files.add(filename)

  color = better_exchook.Color()
  total_relevant_count = 0
  file_count = None
  last_filename = None
  for filename, line, problem_severity, inspect_class, description in inspections:
    if inspect_class in inspect_class_blacklist:
      continue

    if filename != last_filename:
      if last_filename:
        if last_filename in ignore_count_for_files:
          print("The inspection reports for this file are currently ignored.")
        else:
          print(color.color("The inspection reports for this file are fatal!", color="red"))
        print("travis_fold:end:inspect.%s" % last_filename)
      if filename:
        print("travis_fold:start:inspect.%s" % filename)
        print(color.color(
          "File: %s" % filename, color="black" if filename in ignore_count_for_files else "red"))
      last_filename = filename
      file_count = 0
    if not filename:
      continue
    if filename in ignore_count_for_files and file_count >= 10:
      if file_count == 10:
        print("... (further warnings skipped)")
      file_count += 1
      continue

    msg = "%s:%i: %s %s: %s" % (filename, line, problem_severity, inspect_class, description)
    if inspect_class_not_counted and inspect_class in inspect_class_not_counted:
      print(color.color(msg, color="black"))
    else:
      print(msg)
      if filename not in ignore_count_for_files:
        total_relevant_count += 1
    file_count += 1

  print("Total relevant inspection reports:", total_relevant_count)
  return total_relevant_count


def main():
  """
  Main entry point for this script.
  """
  arg_parser = argparse.ArgumentParser()
  arg_parser.add_argument("--xml")
  arg_parser.add_argument("--pycharm")
  arg_parser.add_argument("--setup_pycharm_only", action="store_true")
  arg_parser.add_argument("--skip_setup_pycharm", action="store_true")
  arg_parser.add_argument("--files", nargs="*")
  args = arg_parser.parse_args()

  from lint_common import ignore_count_for_files
  inspect_kwargs = dict(
    inspect_class_blacklist={
      "PyInterpreterInspection",  # TODO how to select this in PyCharm.idea?
      "SpellCheckingInspection",  # way too much for now... TODO this should be fixed later, probably in PyCharm.idea
      "PyClassHasNoInitInspection",  # not relevant?
    },
    inspect_class_not_counted={
      "PyTypeCheckerInspection",  # too much of these: https://youtrack.jetbrains.com/issue/PY-34893
    },
    ignore_count_for_files=ignore_count_for_files)

  if args.xml:
    if report_inspect_dir(args.xml, **inspect_kwargs) > 0:
      sys.exit(1)
    return

  if args.pycharm:
    pycharm_dir = args.pycharm
    check_pycharm_dir(pycharm_dir)
  else:
    pycharm_dir = install_pycharm()

  if not args.skip_setup_pycharm:
    setup_pycharm_python_interpreter(pycharm_dir=pycharm_dir)
  if args.setup_pycharm_only:
    return

  src_dir = prepare_src_dir(files=args.files)
  res_dir = run_inspect(pycharm_dir=pycharm_dir, src_dir=src_dir)
  if report_inspect_dir(res_dir, **inspect_kwargs) > 0:
    sys.exit(1)


if __name__ == "__main__":
  main()
