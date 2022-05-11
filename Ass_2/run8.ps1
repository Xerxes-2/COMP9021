Write-Host 'polys_8_wrong_1.txt:'
Compare-Object (python .\test_ori.py polys_8_wrong_1.txt) (python .\test_new.py polys_8_wrong_1.txt)