<?php 
	
	$itemPath = $argv[1];

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