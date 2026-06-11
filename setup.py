
from cx_Freeze import setup, Executable

opcoes_build = {
    "packages": ["pygame", "pyttsx3", "pyttsx3.drivers", "pyttsx3.drivers.sapi5",
                 "random", "sys", "math", "datetime"],
    # Inclui as pastas de recursos e o log junto do executavel.
    "include_files": ["bases/", "Recursos/", "log.dat"],
}

setup(
    name="Princess Esc",
    version="1.0",
    description="Jogo lateral em Python com Pygame para a atividade de Pensamento Computacional.",
    options={"build_exe": opcoes_build},
    executables=[Executable("main.py", base=None, target_name="PrincesaEmFuga.exe")],
)
