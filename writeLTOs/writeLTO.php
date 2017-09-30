<?php

$idtextfile = "/Users/RLAS_Admin/Sites/ingest/LTOid.txt";

$ltoA = $_POST["ltoA"];
$ltoB = $_POST["ltoB"];

file_put_contents($idtextfile, $ltoA); 
$write = escapeshellcmd("/usr/local/bin/python3 /Users/RLAS_Admin/Sites/ingest/writeLTOs/writeLTO.py " . $ltoA ." ". $ltoB . " 2>&1");

while (@ ob_end_flush()); // end all output buffers if any

$proc = popen($write, 'r');
echo '<pre>';
while (!feof($proc))
{
	echo fread($proc, 4096);
	@ flush();
}
echo '</pre>';


?>