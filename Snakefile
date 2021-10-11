# Minimal snakefile to test caching locally
rule all:
    output: "helloworld.txt"
    conda: "envs/main.yaml"
    log: "helloworld.log"
    shell:
        "echo Hello world > {output}"
