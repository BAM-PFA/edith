<?php

$AIPdir = "/Users/bampfa/Sites/ingest/uploads";
$lastLTOidUsed = file_get_contents("LTOid.txt");
$command = escapeshellcmd("/usr/local/bin/python3 /Users/bampfa/Sites/ingest/listAIPs.py " . $AIPdir);

$output = shell_exec($command . " 2>&1");
echo $output;

echo "<div>If this all looks good, enter the LTO tape ID for the 'A' drive and hit the INGEST AIPs button to write to tape.</div><br/>
	<div>The last LTO tape ID that was used was:<br/><span style='font-weight:bold'>" . $lastLTOidUsed . "</span></div><br><br>";
echo "<form method='post' action='writeLTO.php'>
	<div>
	   <label for='LTOid'>Please enter the LTO tape ID for the tape in the 'A' drive:</label>
	   <input type='text' name='LTOid' required />
	</div>
	
	<div>
		<input type='submit' name='submit'/>
	</div>

	</form>";

?>