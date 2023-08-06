# slot

Rotates a symlink between multiple different possible options.

## Installation

```bash
pip install slot
```

## Terminology

A `target` is the file name that you are going to be turning into a symbolic link.

A `store` is a repository of data files that act as potential options for a `target`.

An `option` is a data file inside of a store.

## Usage

### Create a new store

(and optionally ingest current file as an `option`)

```bash
Usage: slt stores create [OPTIONS] NAME TARGET

Options:
  --help  Show this message and exit.
```

### Add an option to a store

```bash
Usage: slt stores ingest [OPTIONS] STORE_NAME FILE_NAME

Options:
  -n, --name TEXT       Name of the option this file becomes
  -s, --silent BOOLEAN  Disable user interaction
  --help                Show this message and exit.
```

### List stores

```bash
Usage: slt list [OPTIONS]

Options:
  --help  Show this message and exit.
```

### See available options for a store

```bash
Usage: slt options [OPTIONS] STORE_NAME

Options:
  --help  Show this message and exit.
```
