#!/usr/bin/python2.7.3

import os
import os.path
import tempfile
import subprocess
import time
import signal
import re
import sys
import shutil
import decode_out as dec
import csv
#import autoregtest

#file_locations = os.path.expanduser(os.getcwd())
file_locations = "."
#logisim_location = os.path.join(os.getcwd(),"logisim.jar")
logisim_location = "logisim.jar"


class TestCase():
  """
      Runs specified circuit file and compares output against the provided reference trace file.
  """

  def __init__(self, circfile, tracefile):
    self.circfile  = circfile
    self.tracefile = tracefile

  def __call__(self, typ):
    output = tempfile.TemporaryFile(mode='r+')
    command = ["java","-jar",logisim_location,"-tty","table", self.circfile]
    proc = subprocess.Popen(command,
                            stdin=open(os.devnull),
                            stdout=subprocess.PIPE)
    try:
      reference = open(self.tracefile)
      debug_buffer = [] 
      passed = compare_unbounded(proc.stdout,reference,debug_buffer)
    finally:
      os.kill(proc.pid,signal.SIGTERM)
    if passed:
      return (True, "Matched expected output")
    else:
      wtr = csv.writer(sys.stdout, delimiter='\t')
      if not dec.headers(wtr, typ):
        print "CANNOT FORMAT test type=",typ
      else:
          for row in debug_buffer:
	    if(any([not num.find("E")==-1 for num in row])):
		return (False, "Circuit outputs error values")
            wtr.writerow([dec.bin2hex(b) for b in row[0].split('\t')])
            wtr.writerow([dec.bin2hex(b) for b in row[1].split('\t')])

      return (False, "Did not match expected output")

def compare_unbounded(student_out, reference_out, debug):
  while True:
    line1 = student_out.readline().rstrip()
    line2 = reference_out.readline().rstrip()
    debug.append((line1, line2))
   
    if line2 == '':
      break
    if line1 != line2:
      return False
  return True

def run_tests(tests):
  # actual submission testing code
  print "Testing files..."
  tests_passed = 0
  tests_failed = 0

  for description,test,typ in tests:
    test_passed, reason = test(typ)
    if test_passed:
      print "\tPASSED test: %s" % description
      tests_passed += 1
    else:
      print "\tFAILED test: %s (%s)" % (description, reason)
      tests_failed += 1
  
  print "Passed %d/%d tests" % (tests_passed, (tests_passed + tests_failed))

tests = [
  ("ALU sll test",
                  TestCase(os.path.join(file_locations, 'alu-sll.circ'),
                           os.path.join(file_locations,'reference_output/alu-sll.out')), "alu"),  
  ("ALU srl test",
                  TestCase(os.path.join(file_locations, 'alu-srl.circ'),
                           os.path.join(file_locations, 'reference_output/alu-srl.out')), "alu"), 
  ("ALU sra test",
          TestCase(os.path.join(file_locations,'alu-sra.circ'),
                   os.path.join(file_locations,'reference_output/alu-sra.out')), "alu"),  
  ("ALU add (with overflow) test",
        TestCase(os.path.join(file_locations,'alu-add.circ'),
                 os.path.join(file_locations,'reference_output/alu-add.out')), "alu"),
  ("ALU addu (no overflow) test",
                TestCase(os.path.join(file_locations, 'alu-addu.circ'),
                         os.path.join(file_locations,'reference_output/alu-addu.out')), "alu"), 
  ("ALU sub (with overflow) test",
                  TestCase(os.path.join(file_locations, 'alu-sub.circ'),
                           os.path.join(file_locations,'reference_output/alu-sub.out')), "alu"), 
  ("ALU subu (no overflow) test",
               TestCase(os.path.join(file_locations, 'alu-subu.circ'),
                        os.path.join(file_locations,'reference_output/alu-subu.out')), "alu"), 
  ("ALU and test",
            TestCase(os.path.join(file_locations, 'alu-and.circ'),
                     os.path.join(file_locations,'reference_output/alu-and.out')), "alu"),  
  ("ALU or test",
        TestCase(os.path.join(file_locations, 'alu-or.circ'),
                 os.path.join(file_locations,'reference_output/alu-or.out')), "alu"),
  ("ALU xor test",
            TestCase(os.path.join(file_locations, 'alu-xor.circ'),
                     os.path.join(file_locations,'reference_output/alu-xor.out')), "alu"),
  ("ALU slt test",
                  TestCase(os.path.join(file_locations, 'alu-slt.circ'),
                           os.path.join(file_locations,'reference_output/alu-slt.out')), "alu"), 
  ("ALU sltu test",
                TestCase(os.path.join(file_locations, 'alu-sltu.circ'),
                         os.path.join(file_locations,'reference_output/alu-sltu.out')), "alu"), 
  ("RegFile read/write test",
        TestCase(os.path.join(file_locations,'regfile-read_write.circ'),
                 os.path.join(file_locations,'reference_output/regfile-read_write.out')), "regfile"),
  ("RegFile $zero test",
        TestCase(os.path.join(file_locations,'regfile-zero.circ'),
                 os.path.join(file_locations,'reference_output/regfile-zero.out')), "regfile"),
  ("Autogenerated regfile test",
	TestCase(os.path.join(file_locations,'regtest-harness.circ'),
                 os.path.join(file_locations,'reference_output/regtest.out')), "regfile")
]

# 2 stage pipeline tests
p2_tests = [
  ("CPU starter test",
        TestCase(os.path.join(file_locations,'CPU-starter_kit_test.circ'),
                 os.path.join(file_locations,'reference_output/CPU-starter_kit_test.out')), "cpu")
]

# Single-cycle (sc) tests
p2sc_tests = [
  ("CPU starter test",
        TestCase(os.path.join(file_locations,'CPU-starter_kit_test.circ'),
                 os.path.join(file_locations,'reference_output/CPU-starter_kit_test.sc.out')), "cpu"),
  #("func test",
        #TestCase(os.path.join(file_locations,'func_test.circ'),
                 #os.path.join(file_locations,'reference_output/func_test.sc.out')), "cpu-end"), 
  ("test1",
        TestCase(os.path.join(file_locations, 'test1.circ'),
                 os.path.join(file_locations, 'reference_output/test1.sc.out')), "cpu-end"),
  ("test2",
        TestCase(os.path.join(file_locations, 'test2.circ'),
                 os.path.join(file_locations, 'reference_output/test2.sc.out')), "cpu-end"),
  ("test3",
        TestCase(os.path.join(file_locations, 'test3.circ'),
                 os.path.join(file_locations, 'reference_output/test3.sc.out')), "cpu-end"),
  ("test4",
        TestCase(os.path.join(file_locations, 'test4.circ'),
                 os.path.join(file_locations, 'reference_output/test4.sc.out')), "cpu-end"),  
  ("test5",
        TestCase(os.path.join(file_locations, 'test5.circ'),
                os.path.join(file_locations, 'reference_output/test5.sc.out')), "cpu-end"),
  ("test6",
       TestCase(os.path.join(file_locations, 'test6.circ'),
                os.path.join(file_locations, 'reference_output/test6.sc.out')), "cpu-lite"),   
  
]

if __name__ == '__main__':
  if len(sys.argv) < 2:
    print("Usage: " + sys.argv[0] + " (p1|p2)")
    sys.exit(-1)
  if sys.argv[1] == 'p1':
    run_tests(p1_tests)
  elif sys.argv[1] == 'p2':
    run_tests(p2_tests)
  elif sys.argv[1] == 'p2sc':
    run_tests(p2sc_tests)
  else:
    print("Usage: " + sys.argv[0] + " (p1|p2)")
    sys.exit(-1)
