
chrome.tabs.create({
    //windowId: wId,
    index: 0,
    url: 'http://www.yourong.cn/',
    active: true,
    pinned: false,
    //openerTabId: 1
}, function(tab){
    console.log(tab);
});


chrome.tabs.create({
    //windowId: wId,
    index: 0,
    url: 'http://www.huirendai.com/',
    active: true,
    pinned: false,
    //openerTabId: 2
}, function(tab){
    console.log(tab);
});
