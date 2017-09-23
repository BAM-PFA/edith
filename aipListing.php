<?php 
	
	$itemPath = $argv[1];

	// foreach(glob(dirname(__FILE__) .$itemPath . '/*') as $filename){
	// 	echo $filename;
	// 	$filename = basename($filename);
	// 	echo "<option value='" . $filename . "'>".$filename."</option>";
	// }

	// echo "hello there" . $itemPath

	// foreach (new RecursiveIteratorIterator(new RecursiveDirectoryIterator($itemPath)) as $filename)
	// {
	//         echo "<option value='" . $filename . "'>".$filename."</option>";
	// 		// echo "hello there" . $itemPath;
	// }

if ( ! function_exists('glob_recursive'))
{
	function glob_recursive($itemPath, $flags = 0)
   {
     $files = glob($itemPath, $flags);
     foreach (glob(dirname($itemPath).'/*', GLOB_ONLYDIR|GLOB_NOSORT) as $dir)
     {
       $files = array_merge($files, glob_recursive($dir.'/'.basename($itemPath), $flags));
     }
     return $files;
   }

}

?>