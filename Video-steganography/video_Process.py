import Stegno_image
import getpass
import cv2
import os
import subprocess
import math
from termcolor import cprint
from pyfiglet import figlet_format
from rich import print
from rich.console import Console
from rich.table import Table

temp_folder = "frame_folder"
console = Console()
lossless_output = "final_lossless.mkv"


def run_command(cmd):
    try:
        subprocess.run(
            cmd,
            stdout=subprocess.DEVNULL,
            stderr=subprocess.DEVNULL,
            check=True,
        )
        return True
    except (subprocess.CalledProcessError, FileNotFoundError):
        return False


def split_string(s_str, count=10):
    per_c = math.ceil(len(s_str) / count)
    c_cout = 1
    out_str = ""
    split_list = []
    for s in s_str:
        out_str += s
        c_cout += 1
        if c_cout == per_c:
            split_list.append(out_str)
            out_str = ""
            c_cout = 0
    if c_cout != 0:
        split_list.append(out_str)
    return split_list


def createTmp():
    if not os.path.exists(temp_folder):
        os.makedirs(temp_folder)


def clearTmp():
    if not os.path.exists(temp_folder):
        return
    images = [img for img in os.listdir(temp_folder) if img.endswith(".png")]
    for img in images:
        os.remove(os.path.join(temp_folder, img))


def countFrames(path):
    cap = cv2.VideoCapture(path)
    length = int(cap.get(cv2.CAP_PROP_FRAME_COUNT))
    cap.release()
    return length


# Function to extract frames
def FrameCapture(path, op, password, message=""):
    createTmp()
    if op == 1:
        clearTmp()
    split_string_list = split_string(message)
    outputMessage = ""
    if op == 1:
        vidObj = cv2.VideoCapture(path)
        count = 0
        total_frame = countFrames(path)
        position = 0

        while count < total_frame:
            success, image = vidObj.read()
            if not success:
                break

            frame_path = os.path.join(temp_folder, f"frame{count}.png")
            cv2.imwrite(frame_path, image)

            if position < len(split_string_list):
                print(
                    "Input in image working :- ",
                    split_string_list[position],
                )
                Stegno_image.main(
                    op,
                    password=password,
                    message=split_string_list[position],
                    img_path=frame_path,
                )
                position += 1
                os.remove(frame_path)

            count += 1

        vidObj.release()
    elif op == 2:
        images = sorted(
            [
                img
                for img in os.listdir(temp_folder)
                if img.endswith(".png") and img.startswith("frame")
            ],
            key=lambda name: int(name.replace("frame", "").replace(".png", "")),
        )

        for img_name in images:
            frame_path = os.path.join(temp_folder, img_name)
            str = Stegno_image.main(
                op,
                password=password,
                img_path=frame_path,
            )
            if str == "Invalid data!":
                break
            outputMessage = str

    if op == 1:
        print("[cyan]Please wait....[/cyan]")
        makeVideoFromFrame()

    if op == 2:
        print("[green]Message is :-\n[bold]%s[/green]" % outputMessage)
        clearTmp()


def makeVideoFromFrame():
    images = [img for img in os.listdir("frame_folder") if img.endswith(".png")]
    for img in images:
        if img.count("-enc") == 1:
            newImgName = img.split("-")[0] + ".png"
            os.rename(os.path.join("frame_folder", img), os.path.join("frame_folder", newImgName))

    run_command(
        [
            "ffmpeg",
            "-framerate",
            "29.92",
            "-i",
            os.path.join("frame_folder", "frame%d.png"),
            "-c:v",
            "png",
            "-pix_fmt",
            "rgb24",
            "output_lossless.mkv",
            "-y",
        ]
    )
    clearTmp()


def main():
    text = "Video"
    print("Choose one: ")
    print("[cyan]1. Encode[/cyan]\n[cyan]2. Decode[/cyan]")
    op = int(input(">> "))

    if op == 1:
        print(f"[cyan]{text} path (with extension): [/cyan]")
        img = os.path.normpath(input(">> ").strip())

        if not os.path.exists(img):
            print("[red]Error: video file not found.[/red]")
            return

        print("[cyan]Message to be hidden: [/cyan]")
        message = input(">> ")
        password = ""

        print(
            "[cyan]Password to encrypt (leave empty if you want no password): [/cyan]"
        )
        password = getpass.getpass(">> ")

        if password != "":
            print("[cyan]Re-enter Password: [/cyan]")
            confirm_password = getpass.getpass(">> ")
            if password != confirm_password:
                print("[red]Passwords don't match try again [/red]")
                return

        run_command(["ffmpeg", "-i", img, "-q:a", "0", "-map", "a", "sample.mp3", "-y"])

        FrameCapture(img, op, password, message)

        if os.path.exists("output_lossless.mkv"):
            if os.path.exists("sample.mp3"):
                muxed = run_command(
                    [
                        "ffmpeg",
                        "-i",
                        "output_lossless.mkv",
                        "-i",
                        "sample.mp3",
                        "-c:v",
                        "copy",
                        "-c:a",
                        "copy",
                        lossless_output,
                        "-y",
                    ]
                )
                if not muxed:
                    os.replace("output_lossless.mkv", lossless_output)
            else:
                os.replace("output_lossless.mkv", lossless_output)

            if os.path.exists("output_lossless.mkv"):
                os.remove("output_lossless.mkv")
            print(f"[green]Encoding complete. Output saved as [bold]{lossless_output}[/bold][/green]")
        else:
            print("[red]Error: output video was not created. Check if ffmpeg is installed and video format is supported.[/red]")

        if os.path.exists("sample.mp3"):
            os.remove("sample.mp3")

    elif op == 2:
        print(f"[cyan]{text} path (with extension):[/cyan] ")
        img = os.path.normpath(input(">>").strip())

        if not os.path.exists(img):
            print("[red]Error: video file not found.[/red]")
            return

        print("[cyan]Enter password (leave empty if no password):[/cyan] ")
        password = getpass.getpass(">>")
        clearTmp()
        run_command(["ffmpeg", "-i", img, os.path.join(temp_folder, "frame%d.png"), "-y"])
        FrameCapture(img, op, password)


# To remove Credit in starting commnet this function only.
def print_credits():
    table = Table(show_header=True)
    table.add_column("Student Name", style="yellow")
    table.add_column("USN", style="yellow")
    table.add_row("Shashank C", "4NI22CS196")
    table.add_row("Pranav P", "4NI22CS151")
    table.add_row("Pranav Ramesh", "4NI22CS152")
    table.add_row("Prajval Prasad", "4NI22CS144")
    table.add_row("Nidhishree", "4NI22CS138")
    console.print(table)


if __name__ == "__main__":
    os.system("cls" if os.name == "nt" else "clear")
    cprint(figlet_format("STEGANO", font="starwars"), "yellow", attrs=["bold"])
    print_credits()
    print()
    print(
        "[bold]VIDEOHIDE[/bold] allows you to hide texts inside an video. You can also protect these texts with a password using AES-256."
    )
    print()
    main()

# -----------------------
