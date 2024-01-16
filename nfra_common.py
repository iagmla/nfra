import subprocess

def run_shell_command(
    command = list[str]
) -> list[bool, str, str]:
    result = True
    s = subprocess.Popen(command, stdin=subprocess.PIPE, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    stdout, stderr = s.communicate()
    returncode = s.returncode
    if s.returncode != 0:
        result = False
    return [result, stdout, stderr]
