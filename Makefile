default: rear_stand.stl peg.stl keyboard_case_dxfs/keyboard_case_1.dxf case.stl

rear_stand.stl: rear_stand.py
	python3 $<

peg.stl: peg.py
	python3 $<

keyboard_case_dxfs/keyboard_case_1.dxf: keyboard_case.py
	python3 $<

case.stl: case.py
	python3 $<

clean:
	rm *.stl
	rm *.dxf
	rm -Rf keyboard_case_dxfs
