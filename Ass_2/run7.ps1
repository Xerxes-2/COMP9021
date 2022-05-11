Write-Host 'polys_7_test5.txt:'
Compare-Object (python .\test_ori.py polys_7_test5.txt) (python .\test_new.py polys_7_test5.txt)