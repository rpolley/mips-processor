p1:
	cp alu.circ regfile.circ tests
	cd tests && python autoregtest.py && python ./sanity_test.py | tee ../TEST_LOG
