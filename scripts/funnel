#!/usr/bin/env python
# it's a shell script hidden as a python script!
import argparse

from funnel.cmd import preview, build


def main():
  parser = argparse.ArgumentParser()
  parser.add_argument("command", choices=["build", "preview"], help="builds the static site or preview it")
  parser.add_argument("root", help="the root directory that the funnel source resides in. defaults to pwd", nargs="?", default=".")
  parser.add_argument("-t", "--target", help="the target directory for build", default="build")
  args = parser.parse_args()

  if args.command == "preview":
    preview(args.root)
  elif args.command == "build":
    build(args.root, target=args.target)


if __name__ == "__main__":
  main()
