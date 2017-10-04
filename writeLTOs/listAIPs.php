<?php

$AIPdir = "/Volumes/maxxraid1/LTO_STAGE/";
$lastLTOidUsed = file_get_contents("../LTOid.txt");
$command = escapeshellcmd("/usr/local/bin/python3 /Users/RLAS_Admin/Sites/ingest/writeLTOs/listAIPs.py " . $AIPdir);

$output = shell_exec($command . " 2>&1");
echo $output;

echo
// echo "<div>If this all looks good, enter the LTO tape ID for the 'A' drive and hit <br/>CHECK MOUNT<br/>
			// to see if Tape A and Tape B are both mounted and ready to write to.<br/>Then hit the INGEST AIPs button to write to tape.</div><br/>
	"<div>The last LTO tape ID that was used was:<br/><span style='font-weight:bold'>" . $lastLTOidUsed . "</span></div><br><br>";

echo "<div>
		
	</div>";



echo "<form method='post' action=''>

	<div>
	   <label for='LTOid'>Please enter the LTO tape ID for the tape in the 'A' drive:</label>
	   <input type='text' name='LTOid' required />
	</div>
	
	<div>
		<input type='submit' name='tapeIDsubmit' value='CHECK MOUNT STATUS'/>
	</div>
		<?php 

	echo $ltoID; ?>
	</form>";

if(isset($_POST['tapeIDsubmit'])){
$ltoA = $_POST['LTOid'];
$ltoB = str_replace("A","B",$ltoA);

$ltos = array("A" => $ltoA, "B" => $ltoB);

foreach ($ltos as $key => $value) {
	
	echo "<div>The Tape ID for the ".$key." drive is: <span style='font-weight:bold'>".$value."</span>.<br/><br/>Currently checking if the tape is mounted.</div>";
	$checkMount = escapeshellcmd("/usr/local/bin/python3 /Users/RLAS_Admin/Sites/ingest/writeLTOs/checkMount.py ".$value);
	while (@ ob_end_flush()); // end all output buffers if any

	$proc = popen($checkMount, 'r');
	// echo '<pre>';
	while (!feof($proc))
	{
	    echo fread($proc, 4096);
	    @ flush();
	}
	// echo '</pre>';


}

// echo "<div>The Tape ID for the A drive is: <span style='font-weight:bold'>".$ltoA."</span>.<br/>Currently checking if the tape is mounted.</div>";
// 	$checkMountA = escapeshellcmd("/usr/local/bin/python3 /Users/RLAS_Admin/Sites/ingest/writeLTOs/checkMount.py ".$ltoA);
// 	$outputA = shell_exec($checkMountA . " 2>&1");
// 	echo $outputA;

// echo "<br/><br/><div>The Tape ID for the B drive is: <span style='font-weight:bold'>".$ltoB."</span>.<br/>Currently checking if the tape is mounted.</div><br/>";
// 	$checkMountB = escapeshellcmd("/usr/local/bin/python3 /Users/RLAS_Admin/Sites/ingest/writeLTOs/checkMount.py ".$ltoB);
// 	$outputB = shell_exec($checkMountB . " 2>&1");
// 	echo $outputB;


echo "<form method='post' action='writeLTO.php'>
	<div>
	   <input type='hidden' name='ltoA' value=".$ltoA." />
	   <input type='hidden' name='ltoB' value=".$ltoB." />
	   <label for='ingest'><br><br>Once both drives are mounted you can press INGEST: </label>
	   <input type='submit' name='ingest' value='INGEST' />
	</div>
	</form>";

}


?>