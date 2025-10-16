# MLTIF Makefile

all:
	@echo "Use this Makefile to build/configure P4 program and start controller"

p4-compile:
	p4c-bm2-ss --p4v 16 itam/itam.p4 -o configs/

run:
	python3 runtime/mltif_controller.py
