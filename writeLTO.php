<?php

$idtextfile = "/Users/bampfa/Sites/ingest/LTOid.txt";

$LTOid = $_POST["LTOid"];
$command = escapeshellcmd("/usr/local/bin/python3 /Users/bampfa/Sites/ingest/writeLTO.py " . $LTOid);
$output = shell_exec($command . " 2>&1");
echo $output;

file_put_contents($idtextfile, $LTOid);

?>