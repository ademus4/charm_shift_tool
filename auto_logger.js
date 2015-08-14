var page = require('webpage').create(), loadInProgress = false, fs = require('fs');
var htmlFiles = ['http://ps-irrad.web.cern.ch/irrad/intensityAll.php','http://ps-irrad.web.cern.ch/irrad/bpm.php?bpmid=BPM_01','http://thornton.web.cern.ch/charm_mwpc.html','https://op-webtools.web.cern.ch/op-webtools/vistar/vistars.php?usr=CPS'];
var images = ['//cern.ch/dfs/Websites/t/test-charmShiftTool/screens/bpm_all', '//cern.ch/dfs/Websites/t/test-charmShiftTool/screens/bpm1', '//cern.ch/dfs/Websites/t/test-charmShiftTool/screens/mwpc', '//cern.ch/dfs/Websites/t/test-charmShiftTool/screens/op'];
 
console.log('Number of Html Files: ' + htmlFiles.length);
var width = 1920;
var height = 1080;
page.viewportSize = { width: width, height: height};
 
// output pages as PNG
var url_index = 0;
 
var interval = setInterval(function() {
    if (!loadInProgress && url_index < htmlFiles.length) {
        console.log("image " + (url_index + 1));
        page.open(htmlFiles[url_index]);
    }
    if (url_index == htmlFiles.length) {
        console.log("image render complete!");
        phantom.exit();
    }
}, 250); // load timeout
 
page.onLoadStarted = function() {
    loadInProgress = true;
    console.log('page ' + (url_index + 1) + ' load started');
};
 
page.onLoadFinished = function() {
    window.setTimeout(function () {
      loadInProgress = false;
      console.log(images[url_index] + ' load finished');
      page.render(images[url_index]+ ".png");
      url_index++;
    }, 5000); // Timeout to allow sufficient time for rendring 
}
