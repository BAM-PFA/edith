<?php
	$user = $_POST["user"];
	$fileArray = [];
	foreach($_FILES['file']['tmp_name'] as $key => $tmp_name ){
	    $file_name = $_FILES['file']['name'][$key];
	    // $file_size = $_FILES['file']['size'][$key];
	    $file_tmp = $_FILES['file']['tmp_name'][$key];
	    // $file_type = $_FILES['file']['type'][$key];
	    // $fileArray[] = [$file_tmp => $file_name];


		$metadataStatus = "reject";
		$basename = basename($file_name);
		// echo $basename;
		include 'metadataFetch.php'; 
		echo "<div>Does this look ok? </div>";
		echo '<form method="post">
			<div>
			   <label for="accept">Accept</label>
			   <input type="radio" name="accept" <?php if (isset($accept) && $metadataStatus = "accept"); ?> <br/>
			</div>
			</form>';
	    $fileArray[] = [$file_tmp => ["status" => $metadataStatus]];
		

	}


	
	print_r($fileArray)

	
	// echo '<form method="post" action="ingest.php">
	// 		<div>
	// 		   <!-- <input type="hidden">$file_name = $_FILES['file']['name'][$key];-->
	// 		   <input type="submit" value="INGEST!"/><br/> 
	// 		</div>
	// 	</form>';



?>