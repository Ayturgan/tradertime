from cx_Freeze import setup, Executable

# Настройки
build_exe_options = {
    "packages": ["customtkinter", "pygame", "tkinter", "time"],
    "include_files": ["sound.mp3"]
}
# Основная настройка
setup(
    name="TradeTimer",
    version="0.1",
    description="Timer Application",
    options={"build_exe": build_exe_options},
    executables=[Executable("main.py", icon="icon.ico", base="Win32GUI")]
)
