<?php

$idtextfile = "/Users/RLAS_Admin/Sites/ingest/LTOid.txt";

$ltoA = $_POST["ltoA"];
$ltoB = $_POST["ltoB"];

file_put_contents($idtextfile, $ltoA); 
$command = escapeshellcmd("/usr/local/bin/python3 /Users/RLAS_Admin/Sites/ingest/writeLTOs/writeLTO.py " . $ltoA ." ". $ltoB);
$output = shell_exec($command . " 2>&1");
echo "<div>".$output."</div>";




?>