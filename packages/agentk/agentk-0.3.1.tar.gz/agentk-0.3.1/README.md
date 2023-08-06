# "k"

## TLDR;

Install the "k" by either doing: 

	pip install agentk

(Yes, ^^ it is written in python and your OS needs to have recent version 2 or 3)

or copying it in some bin folder on your PATH and running `pip install -r requirements.txt`


---

 > "A person is smart. People are dumb, panicky, dangerous animals, and you know it." -- Agent K

#### "AGENT" K is a complete minimalistic kubectl "doner"-wrap

Obviously, as a short-hand wrapper, **k** can do everything **kubectl** already can, but it is (a) shorter and (b) adds few tricks like merging configs and switching contexts .. (k) feeds back to the *kubectl* command-line those args which it does not want to intercept or handle.

## Usage

The following is equivalent:

	kubectl get pods --all-namespaces
	k get pods -A
	k p -A


### Switching context

Argument-free invocation prompts for context switch options between multiple cluster contexts found in `~/.kube/config`:

	k


### Switching namespaces

One can change the default namespace on the currently active context (`namespace` key in `~/.kube/config`) using either of two equivalent commands:

	kubectl config set-context $(kubectl config current-context) --namespace foo
	k sn foo

The last command is a `k` shortcut.


### Shortcuts to get resources

You can find the full list of shortcuts defined as the dictionary inside the `k` script. In particular that would be:

    # resource
    "ev": "event",
    "ep": "endpoints",
    "p": "pod",
    "s": "service",
    "v": "volume",
    "n": "node",
    "dp": "deployment",
    "st": "statefulset",
    "in": "ingress",
    "ns": "namespace",

At the end of the list there are one letter action-shortcuts:

    # actions
    "c": "create",
    "a": "apply",
    "d": "delete",

This means that the following is equivalent:

	kubectl apply -f <foo-k8s-manifest.yaml>
	k a -f <foo-k8s-manifest.yaml>


## Develop

To remind, you can do `pip install -e .` in order to utilize developer mode.

## Installation in the cloud

If you work with `kubectl` without a privileged or super-user access, for example inside a corporate network or in a cloud-shell (but you still have access to python), then your installation will look like:

	pip install --user agentk

This will install the script in your local `$HOME` folder.

Don't forget to append your `~/.bashrc` or `~/bash_profile` or other shell-rc file with:

	export PATH="$HOME/.local/bin:$PATH"

## Command completion

You can put this into your `.bashrc` to get alias and auto completion for `k` similar as for `kubectl`:

```
source <(kubectl completion bash | sed s/kubectl/k/g)
```

Similar works well for **zsh**.
