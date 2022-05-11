Write-Host 'polys_5_incorrect_1.txt:'
Compare-Object (python .\test_ori.py polys_5_incorrect_1.txt) (python .\test_new.py polys_5_incorrect_1.txt)