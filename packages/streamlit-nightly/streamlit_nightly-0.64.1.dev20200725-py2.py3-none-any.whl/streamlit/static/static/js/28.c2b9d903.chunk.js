(this["webpackJsonpstreamlit-browser"]=this["webpackJsonpstreamlit-browser"]||[]).push([[28],{2094:function(t,e,i){},2374:function(t,e,i){"use strict";i.r(e);var n,a=i(0),r=i.n(a),s=i(205),c=i(49);i(2094);!function(t){t[t.OriginalWidth=-1]="OriginalWidth",t[t.ColumnWidth=-2]="ColumnWidth"}(n||(n={}));class l extends a.PureComponent{render(){const t=this.props,e=t.element,i=t.width,a=t.height,s=t.isFullScreen;let l;const o=e.get("width");if(o===n.OriginalWidth)l=void 0;else if(o===n.ColumnWidth)l=i;else{if(!(o>0))throw Error("Invalid image width: ".concat(o));l=e.get("width")}const d={};return a&&s?(d.height=a,d["object-fit"]="contain"):d.width=l,r.a.createElement("div",{style:{width:i}},e.get("imgs").map((t,e)=>r.a.createElement("div",{className:"image-container stImage",key:e,style:{width:l}},r.a.createElement("img",{style:d,src:Object(c.b)(t.get("url")),alt:e}),!s&&r.a.createElement("div",{className:"caption"}," ",t.get("caption")," "))))}}var o=Object(s.a)(l);i.d(e,"default",(function(){return o}))}}]);
//# sourceMappingURL=28.c2b9d903.chunk.js.map