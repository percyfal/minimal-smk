# Minimal snakefile to test caching locally
rule all:
    output: "helloworld.txt.gz"
    conda: "envs/main.yaml"
    log: "helloworld.log"
    shell:
        "echo Hello world | gzip -c > {output}"
