Write-Host 'polys_6_incorrect_2.txt:'
Compare-Object (python .\test_ori.py polys_6_incorrect_2.txt) (python .\test_new.py polys_6_incorrect_2.txt)