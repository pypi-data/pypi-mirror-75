# dapeng-cli

Command line tool for Dapeng system. You can work with Dapeng
in terminal by command `dapeng`.

- Create new jobs on Dapeng.
- Run test on remote. (dpc-lite)
- Rerun exists Dapeng task.
- Verify exists Dapeng task in a new session.

```shell
$ dapeng --help
Usage: dapeng [OPTIONS] COMMAND [ARGS]...

Options:
  -log PATH  log console output to file
  --debug    enable debug level
  --help     Show this message and exit.

Commands:
  new     create new jobs on Dapeng
  rerun   rerun dapeng task
  test    run a test on remote
  verify  verify dapeng tasks
```

# Installation

```shell
pip install dapeng-cli -U
```

# Usage

- Test application on cloud

```shell
dapeng test -f hello_world.out -n hello_world -b frdmk64f
```

- Rerun Dapeng task

```shell
dapeng rerun -id <case_id>
```

- Verify Dapeng tasks

```shell
dapeng verify -id <case_id>
```



