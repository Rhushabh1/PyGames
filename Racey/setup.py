import cx_Freeze 

executables = [cx_Freeze.Executable("basic.py")]

cx_Freeze.setup(
	name = "A Bit Racey",
	options = {"build_exe": {"packages":["pygame"],
							"include_files":["racecar.png"]}},
	executables = executables

	)