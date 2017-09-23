<?php

<<<<<<< HEAD
$idtextfile = "/Users/RLAS_Admin/Sites/ingest/LTOid.txt";

$LTOid = $_POST["LTOid"];
$command = escapeshellcmd("/usr/local/bin/python3 /Users/RLAS_Admin/Sites/ingest/writeLTO.py " . $LTOid);
=======
$idtextfile = "/Users/bampfa/Sites/ingest/LTOid.txt";

$LTOid = $_POST["LTOid"];
$command = escapeshellcmd("/usr/local/bin/python3 /Users/bampfa/Sites/ingest/writeLTO.py " . $LTOid);
>>>>>>> 0d8bef369fff3d1ce9f5033849dfa0d53549029e
$output = shell_exec($command . " 2>&1");
echo $output;

file_put_contents($idtextfile, $LTOid);

?>