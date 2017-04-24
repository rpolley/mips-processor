p2sc:
	cp alu.circ regfile.circ mem.circ cpu.circ tests
	cd tests && python2.7 ./autoregtest.py && python2.7 ./sanity_test.py p2sc | tee ../TEST_LOG

p2:
	cp alu.circ regfile.circ mem.circ cpu.circ tests
	cd tests && python2.7 autoregtest.py && python2.7 ./sanity_test.py p2 | tee ../TEST_LOG

p1:
	cp alu.circ regfile.circ tests
	cd tests && python2.7 autoregtest.py && python2.7 ./sanity_test.py p1 | tee ../TEST_LOG

