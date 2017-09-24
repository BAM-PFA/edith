<?php

$idtextfile = "/Users/RLAS_Admin/Sites/ingest/LTOid.txt";

$LTOid = $_POST["LTOid"];
$command = escapeshellcmd("/usr/local/bin/python3 /Users/RLAS_Admin/Sites/ingest/writeLTO.py " . $LTOid);

$output = shell_exec($command . " 2>&1");
echo $output;

file_put_contents($idtextfile, $LTOid);

?>