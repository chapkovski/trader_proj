(function(e){function t(t){for(var a,s,o=t[0],c=t[1],l=t[2],d=0,g=[];d<o.length;d++)s=o[d],Object.prototype.hasOwnProperty.call(r,s)&&r[s]&&g.push(r[s][0]),r[s]=0;for(a in c)Object.prototype.hasOwnProperty.call(c,a)&&(e[a]=c[a]);u&&u(t);while(g.length)g.shift()();return i.push.apply(i,l||[]),n()}function n(){for(var e,t=0;t<i.length;t++){for(var n=i[t],a=!0,o=1;o<n.length;o++){var c=n[o];0!==r[c]&&(a=!1)}a&&(i.splice(t--,1),e=s(s.s=n[0]))}return e}var a={},r={main:0},i=[];function s(t){if(a[t])return a[t].exports;var n=a[t]={i:t,l:!1,exports:{}};return e[t].call(n.exports,n,n.exports,s),n.l=!0,n.exports}s.m=e,s.c=a,s.d=function(e,t,n){s.o(e,t)||Object.defineProperty(e,t,{enumerable:!0,get:n})},s.r=function(e){"undefined"!==typeof Symbol&&Symbol.toStringTag&&Object.defineProperty(e,Symbol.toStringTag,{value:"Module"}),Object.defineProperty(e,"__esModule",{value:!0})},s.t=function(e,t){if(1&t&&(e=s(e)),8&t)return e;if(4&t&&"object"===typeof e&&e&&e.__esModule)return e;var n=Object.create(null);if(s.r(n),Object.defineProperty(n,"default",{enumerable:!0,value:e}),2&t&&"string"!=typeof e)for(var a in e)s.d(n,a,function(t){return e[t]}.bind(null,a));return n},s.n=function(e){var t=e&&e.__esModule?function(){return e["default"]}:function(){return e};return s.d(t,"a",t),t},s.o=function(e,t){return Object.prototype.hasOwnProperty.call(e,t)},s.p="/front/";var o=window["webpackJsonp"]=window["webpackJsonp"]||[],c=o.push.bind(o);o.push=t,o=o.slice();for(var l=0;l<o.length;l++)t(o[l]);var u=c;i.push([0,"chunk-vendors"]),n()})({0:function(e,t,n){e.exports=n("56d7")},"034f":function(e,t,n){"use strict";n("85ec")},"56d7":function(e,t,n){"use strict";n.r(t);n("e260"),n("e6cf"),n("cca6"),n("a79d");var a=n("a026"),r=function(){var e=this,t=e.$createElement,n=e._self._c||t;return n("v-app",{attrs:{app:""}},[e.training?n("v-system-bar",{staticClass:"d-flex justify-center align-center",attrs:{dark:"",color:"red"}},[n("div",[e._v("Training round!")])]):e._e(),n("transition",{attrs:{"enter-active-class":"animate__animated animate__bounce animate__slow","leave-active-class":"animate__animated animate__fadeOutTopRight animate__slow"}},[e.isAwardGiven&&e.gamified?n("v-overlay",{attrs:{value:e.isAwardGiven,dark:!1,opacity:0,"z-index":"10000"}},[n("div",{staticClass:"d-flex flex-column justify-center align-center"},[n("v-img",{attrs:{contain:"","max-height":"300","max-width":"300",src:e.awardJustGiven.img}}),n("v-card",{attrs:{elevation:"3"}},[n("v-card-title",{staticClass:"d-flex align-center justify-center text-center"},[n("div",[e._v(e._s(e.awardJustGiven.name))])]),n("v-card-text",[e._v(" "+e._s(e.awardJustGiven.desc)+" ")])],1)],1)]):e._e()],1),e.gamified?n("v-overlay",{attrs:{value:e.showHappyFace}},[n("div",{staticClass:"d-flex flex-column align-center justify-center"},[n("img",{attrs:{src:"https://i.gifer.com/Llx5.gif",alt:"",height:"300px",width:"600px"}}),n("h1",[e._v("We are so happy to see back!")])])]):e._e(),e.gamified?n("div",{staticClass:"funnyam d-flex flex-column"},[n("transition",{attrs:{name:"custom-classes-transition","enter-active-class":"animate__animated animate__bounceIn",appear:""}},[e.currentMessage?n("speech-bubble",{attrs:{text:e.currentMessage}}):e._e()],1),n("img",{staticStyle:{"align-self":"flex-end"},attrs:{src:"https://www.picgifs.com/graphics/s/scrooge-mcduck/graphics-scrooge-mcduck-940725.gif",alt:"",height:"150px",width:"150px"}})],1):e._e(),n("transition",{attrs:{name:"fade"}},[e.snackbar?n("particles-bg",{attrs:{config:e.pconfig,type:e.particle_type,bg:!1,canvas:{position:"absolute",zIndex:1e3,top:0,left:0}}}):e._e()],1),n("input",{attrs:{type:"hidden",name:"exit_price"},domProps:{value:e.currentPrice}}),n("v-app-bar",{style:e.getMenuStyle,attrs:{app:"","clipped-left":"",height:"100"}},[n("instructions-dialog"),n("v-sheet",{staticClass:"d-flex align-center ml-1 pa-2 rounded-xl",attrs:{outlined:""}},[n("div",{staticClass:"d-flex align-center font-weight-bold"},[e._v(" Current price: "),n("div",{staticClass:"ml-1 pa-2 text-no-wrap",class:e.gamified?"blue  white--text rounded-pill":"border rounded-xl black--text"},[e._v(" $"+e._s(e.formattedTween||e.currentPrice)+" ")])])]),n("v-spacer"),n("v-sheet",{staticClass:"d-flex align-center ml-1 pa-2 rounded-xl",attrs:{outlined:""}},[n("div",{staticClass:"d-flex align-center font-weight-bold"},[e._v(" Crash probability (for each price update): "),n("div",{staticClass:"ml-1 pa-2 text-no-wrap rounded-pill",class:e.gamified?"red  white--text rounded-pill":"border rounded-xl black--text"},[e._v(" "+e._s((100*e.probToZero).toFixed(0))+"% ")])])]),n("v-spacer"),e.gamified?n("div",{staticClass:"d-flex"},e._l(e.awards,(function(t){return n("div",{key:t.id,staticClass:"m-1"},[n("v-tooltip",{attrs:{bottom:""},scopedSlots:e._u([{key:"activator",fn:function(a){var r=a.on,i=a.attrs;return[n("div",e._g(e._b({},"div",i,!1),r),[n("v-badge",{attrs:{bordered:"",overlap:"",color:e.locked(t.id)?"secondary":"success",bottom:"",left:""},scopedSlots:e._u([{key:"badge",fn:function(){return[e.locked(t.id)?n("v-icon",[e._v("mdi-lock")]):n("v-icon",[e._v("mdi-check-outline")])]},proxy:!0}],null,!0)},[n("v-avatar",{attrs:{size:"60"}},[n("v-img",{class:e.classAward(t.id),attrs:{src:t.img}})],1)],1)],1)]}}],null,!0)},[n("span",[e._v(e._s(t.brief))])])],1)})),0):e._e(),n("v-btn",{staticClass:"mx-3",attrs:{large:""},on:{click:e.showSellingDialog}},[e._v("Sell")])],1),n("end-dialog",{attrs:{dialog:e.showEndDialog,currentPrice:e.currentPrice},on:{finishGame:e.finishGame}}),n("confirm-dialog",{attrs:{dialog:e.dialog,currentPrice:e.currentPrice},on:{sell:e.sell,continueKeeping:e.continueKeeping}}),e.gamified?n("v-navigation-drawer",{attrs:{clipped:"",app:"",width:"300",color:"blue",permanent:""}},[n("v-card",{staticClass:"d-flex flex-column buysellcard",staticStyle:{height:"100%"},attrs:{"fill-height":""}},[n("v-card-text",{staticClass:"overflow-y-auto",staticStyle:{"margin-bottom":"50px"}},[n("v-list",[n("v-list-item-group",{attrs:{"active-class":"border",color:"indigo"}},[n("transition-group",{attrs:{"enter-active-class":"animate__animated animate__fadeInRight animate__slow","leave-active-class":"animate__animated animate__fadeOutTopRight animate__slow"}},e._l(e.messages,(function(t,a){return n("v-list-item",{key:t,ref:"li_"+a,refInFor:!0,staticClass:"m-3",attrs:{id:"li_"+a,dense:""}},[n("v-list-item-content",{directives:[{name:"breathing-colors",rawName:"v-breathing-colors",value:e.sample,expression:"sample"}],staticClass:"message mb-3 pr-3"},[n("v-list-item-title",{staticClass:"titlestyle",staticStyle:{"white-space":"pre-wrap"},domProps:{innerHTML:e._s(t)}})],1)],1)})),1)],1)],1),n("div",{ref:"listend",attrs:{id:"listend"}},[e._v(" ")])],1)],1)],1):e._e(),n("v-main",{directives:[{name:"show",rawName:"v-show",value:!0,expression:"true"}],attrs:{app:""}},[n("v-container",{attrs:{fluid:""}},[n("v-row",[n("v-col",{attrs:{cols:"12"}},[n("highcharts",{ref:"priceGraph",staticClass:"hc",attrs:{constructorType:"stockChart",options:e.chartOptions,updateArgs:[!0,!0,!0]}})],1)],1)],1)],1),n("v-snackbar",{scopedSlots:e._u([{key:"action",fn:function(t){var a=t.attrs;return[n("v-btn",e._b({attrs:{color:"pink",text:""},on:{click:function(t){e.snackbar=!1}}},"v-btn",a,!1),[e._v(" Close ")])]}}]),model:{value:e.snackbar,callback:function(t){e.snackbar=t},expression:"snackbar"}},[e._v(" "+e._s(e.snackbartext)+" ")])],1)},i=[],s=n("5530"),o=n("1da1"),c=(n("96cf"),n("d3b7"),n("ddb0"),n("b680"),n("159b"),n("caad"),n("2532"),"data:image/png;base64,iVBORw0KGgoAAAANSUhEUgAAAFAAAABQCAYAAACOEfKtAAAAAXNSR0IArs4c6QAAAAlwSFlzAAALEwAACxMBAJqcGAAABCJpVFh0WE1MOmNvbS5hZG9iZS54bXAAAAAAADx4OnhtcG1ldGEgeG1sbnM6eD0iYWRvYmU6bnM6bWV0YS8iIHg6eG1wdGs9IlhNUCBDb3JlIDUuNC4wIj4KICAgPHJkZjpSREYgeG1sbnM6cmRmPSJodHRwOi8vd3d3LnczLm9yZy8xOTk5LzAyLzIyLXJkZi1zeW50YXgtbnMjIj4KICAgICAgPHJkZjpEZXNjcmlwdGlvbiByZGY6YWJvdXQ9IiIKICAgICAgICAgICAgeG1sbnM6dGlmZj0iaHR0cDovL25zLmFkb2JlLmNvbS90aWZmLzEuMC8iCiAgICAgICAgICAgIHhtbG5zOmV4aWY9Imh0dHA6Ly9ucy5hZG9iZS5jb20vZXhpZi8xLjAvIgogICAgICAgICAgICB4bWxuczpkYz0iaHR0cDovL3B1cmwub3JnL2RjL2VsZW1lbnRzLzEuMS8iCiAgICAgICAgICAgIHhtbG5zOnhtcD0iaHR0cDovL25zLmFkb2JlLmNvbS94YXAvMS4wLyI+CiAgICAgICAgIDx0aWZmOlJlc29sdXRpb25Vbml0PjI8L3RpZmY6UmVzb2x1dGlvblVuaXQ+CiAgICAgICAgIDx0aWZmOkNvbXByZXNzaW9uPjU8L3RpZmY6Q29tcHJlc3Npb24+CiAgICAgICAgIDx0aWZmOlhSZXNvbHV0aW9uPjcyPC90aWZmOlhSZXNvbHV0aW9uPgogICAgICAgICA8dGlmZjpPcmllbnRhdGlvbj4xPC90aWZmOk9yaWVudGF0aW9uPgogICAgICAgICA8dGlmZjpZUmVzb2x1dGlvbj43MjwvdGlmZjpZUmVzb2x1dGlvbj4KICAgICAgICAgPGV4aWY6UGl4ZWxYRGltZW5zaW9uPjgwPC9leGlmOlBpeGVsWERpbWVuc2lvbj4KICAgICAgICAgPGV4aWY6Q29sb3JTcGFjZT4xPC9leGlmOkNvbG9yU3BhY2U+CiAgICAgICAgIDxleGlmOlBpeGVsWURpbWVuc2lvbj44MDwvZXhpZjpQaXhlbFlEaW1lbnNpb24+CiAgICAgICAg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"),l=n("5c51"),u=function(){var e=this,t=e.$createElement,n=e._self._c||t;return n("div",{staticClass:"talk-bubble tri-right border btm-right-in round"},[n("div",{staticClass:"talktext"},[n("p",[n("typical",{staticClass:"typicalWrapper",attrs:{steps:[""+e.text,1e3],loop:1,wrapper:"div"}})],1)])])},d=[],g=n("4140"),p=n.n(g),m={name:"SpeechBuuble",props:["text"],components:{typical:p.a},data:function(){return{}},methods:{}},v=m,f=(n("f5da"),n("2877")),h=Object(f["a"])(v,u,d,!1,null,null,null),b=h.exports,w=function(){var e=this,t=e.$createElement,n=e._self._c||t;return n("v-dialog",{attrs:{persistent:"","max-width":"490"},model:{value:e.dialog,callback:function(t){e.dialog=t},expression:"dialog"}},[n("v-card",[n("v-card-title",{staticClass:"text-h5",attrs:{color:"danger"}},[e._v("End of the round")]),n("v-card-text",[n("v-sheet",{staticClass:"d-flex align-center ml-1 pa-2 rounded-xl justify-center",attrs:{outlined:""}},[n("div",{staticClass:"d-flex align-center  font-weight-bold  justify-center"},[n("div",[e._v(" Your payoff: ")]),n("div",{staticClass:"ml-1 pa-2  text-no-wrap rounded-pill",class:e.$gamified?"blue   white--text":"rounded-xl border"},[e._v(" $"+e._s(e.currentPrice)+" ")])])]),e._v(" Click 'Next' to continue to the next round ")],1),n("v-card-actions",[n("v-spacer"),n("v-btn",{class:e.$gamified?"red":"",attrs:{color:" darken-1"},on:{click:e.submit}},[e._v(" Next")])],1)],1)],1)},A=[],C={props:["dialog","currentPrice"],components:{},data:function(){return{}},methods:{submit:function(){this.$emit("finishGame")}}},x=C,I=n("6544"),y=n.n(I),k=n("8336"),P=n("b0af"),V=n("99d9"),R=n("169a"),G=n("8dd9"),j=n("2fa4"),T=Object(f["a"])(x,w,A,!1,null,null,null),O=T.exports;y()(T,{VBtn:k["a"],VCard:P["a"],VCardActions:V["a"],VCardText:V["b"],VCardTitle:V["c"],VDialog:R["a"],VSheet:G["a"],VSpacer:j["a"]});var _=function(){var e=this,t=e.$createElement,n=e._self._c||t;return n("v-dialog",{attrs:{"max-width":"600"},model:{value:e.dialog,callback:function(t){e.dialog=t},expression:"dialog"}},[n("v-card",[n("v-card-title",{staticClass:"text-h5"},[e._v("Selling decision")]),n("v-card-text",[e._v(" Do you really want to sell your asset? If you click 'Sell' this round will be over. ")]),n("v-card-actions",[n("v-spacer"),n("div",[n("v-btn-toggle",[n("v-btn",{class:e.$gamified?"green":"",attrs:{color:" darken-1"},on:{click:e.continueKeeping}},[e._v(" Keep ")]),n("v-btn",{class:e.$gamified?"red":"",attrs:{color:" darken-1"},on:{click:e.sell}},[e._v(" Sell")])],1)],1)],1)],1)],1)},S=[],D={props:["dialog","currentPrice"],components:{},data:function(){return{}},methods:{conditionalSelling:function(e){var t=this;return Object(o["a"])(regeneratorRuntime.mark((function n(){var a;return regeneratorRuntime.wrap((function(n){while(1)switch(n.prev=n.next){case 0:if(1!=t.$socket.readyState){n.next=4;break}return a={name:"slider value changed",sliderValue:e,currentPrice:t.currentPrice},n.next=4,t.$socket.sendObj(a);case 4:0==e&&t.sell();case 5:case"end":return n.stop()}}),n)})))()},sell:function(){this.$emit("sell")},continueKeeping:function(){this.$emit("continueKeeping")}}},L=D,M=n("a609"),W=Object(f["a"])(L,_,S,!1,null,null,null),E=W.exports;y()(W,{VBtn:k["a"],VBtnToggle:M["a"],VCard:P["a"],VCardActions:V["a"],VCardText:V["b"],VCardTitle:V["c"],VDialog:R["a"],VSpacer:j["a"]});var Z=n("4452"),N=n.n(Z),B=n("e703"),z=n("0adb"),Y=n("a959"),H=function(){var e=this,t=e.$createElement,n=e._self._c||t;return n("div",{staticClass:"text-center"},[n("v-dialog",{attrs:{width:"800"},scopedSlots:e._u([{key:"activator",fn:function(t){var a=t.on,r=t.attrs;return[n("v-btn",e._g(e._b({staticClass:"mx-1",attrs:{color:"green white--text",small:""}},"v-btn",r,!1),a),[e._v(" Instructions ")])]}}]),model:{value:e.dialog,callback:function(t){e.dialog=t},expression:"dialog"}},[n("v-card",[n("v-card-title",{staticClass:"text-h5 grey lighten-2"},[e._v(" Instructions ")]),n("v-card-text",{staticClass:"text-left",domProps:{innerHTML:e._s(e.instructions)}}),n("v-divider"),n("v-card-actions",[n("v-spacer"),n("v-btn",{attrs:{color:"primary",text:""},on:{click:e.closeDialog}},[e._v(" Close ")])],1)],1)],1)],1)},X=[],J={data:function(){return{dialog:!1,instructions:document.getElementById("instructions").innerHTML}},methods:{closeDialog:function(){this.dialog=!1}}},F=J,Q=n("ce7e"),U=Object(f["a"])(F,H,X,!1,null,null,null),K=U.exports;y()(U,{VBtn:k["a"],VCard:P["a"],VCardActions:V["a"],VCardText:V["b"],VCardTitle:V["c"],VDialog:R["a"],VDivider:Q["a"],VSpacer:j["a"]});var q=n("cffa"),$=n("2ef0"),ee=n.n($),te=window.max_length,ne=window.starting_price,ae=window.tick_frequency,re={name:"App",components:{highcharts:Z["Chart"],ConfirmDialog:E,EndDialog:O,InstructionsDialog:K,ParticlesBg:l["a"],SpeechBubble:b},data:function(){var e=Date.UTC(2009,0,1),t=Object(B["a"])(Object(z["a"])(new Date,ae*te));return{gamified:window.gamified,training:window.training,currentMessage:null,awardJustGiven:null,isAwardGiven:!1,timeInTrade:0,minx:e,maxx:t,showHappyFace:!1,showLastMsg:!1,particle_type:"fountain",heartConfig:{num:[4,7],rps:.1,radius:[5,40],life:[1.5,3],v:[2,3],tha:[-30,30],body:c,alpha:[.6,0],scale:[.1,.4],position:"all",cross:"dead",random:1},snackbar:!1,snackbartext:null,happyHappens:!1,prices:[],sample:{colors:["red","green","blue"],interval:3e3,transition:{duration:1e3}},showEndDialog:!1,messages:[],zeroCounter:0,grownCounter:0,TwoTwosCounter:0,sensitivity:5,sensitivity2:3,probToZero:window.crash_probability,startingPrice:ne,currentPrice:ne,submittable:!1,onPause:!1,counter:0,startTime:new Date,endTime:null,timeSpent:null,reset:!1,messageMoveDelay:5e3,dialog:!1,tweenedPrice:null,stockInterval:null,tickFrequency:ae,awardsGiven:[],awards:{4:{id:0,img:"https://cdn0.iconfinder.com/data/icons/business-finance-vol-2-56/512/stock_trader_trade_exchange-256.png",name:"Level I",brief:"Level I Badge: Trading intern",desc:["Level up! Doing well 👍","Way to go -- stay strong! 💎🤲","You are definitely going places! 🙌"]},9:{id:1,img:"https://cdn2.iconfinder.com/data/icons/financial-strategy-20/496/trader-bitcoin-cryptocurrency-investment-businessman-1024.png",name:"Level II",brief:"Level II Badge: Trading manager",desc:["Level up again! You belong on the trading floor 🤑","Nerves of steel: stocks are going strong! 📈","Bulls 🐂 are in the arena. Good job!","Have you ever thought of opening your own trading firm?"]},19:{id:2,img:"https://cdn1.iconfinder.com/data/icons/office-and-internet-3/49/217-512.png",name:"Level III",brief:"Level III Badge: Money Boss",desc:["You are the money-maker! 💰","Diamond hands 💎🤲 Impressive run!","To the moon! 🚀 🚀 🚀"]}},chartOptions:{time:{useUTC:!1},yAxis:{startOnTick:!1,endOnTick:!1},xAxis:{startOnTick:!1,endOnTick:!1,showLastLabel:!0,min:Object(B["a"])(new Date),max:Object(B["a"])(Object(z["a"])(new Date,ae*te))},navigator:{enabled:!1},rangeSelector:{enabled:!1,inputEnabled:!1,selected:0},series:[{name:"Stock price",data:[[Object(B["a"])(new Date),ne]]}]}}},computed:{getMenuStyle:function(){return this.training?{top:"25px"}:null},awardTimes:function(){return ee.a.keys(this.awards)},lastMsg:function(){return ee.a.last(this.messages)},pconfig:function(){return"fountain"==this.particle_type?{}:this.heartConfig},formattedTween:function(){return this.tweenedPrice?this.tweenedPrice.toFixed(2):this.currentPrice.toFixed(2)}},watch:{counter:function(e){var t=this;ee.a.forEach(this.awardTimes,(function(n){if(e>n&&!t.awardsGiven.includes(t.awards[n].id)){t.isAwardGiven=!0;var a=t.awards[n];a.desc=ee.a.sample(t.awards[n].desc),t.awardJustGiven=t.awards[n],t.awardsGiven.push(t.awards[n].id),setTimeout((function(){t.isAwardGiven=!1,t.awardJustGiven=null}),3e3)}}))},dialog:function(e){this.onPause=e},messages:function(e){var t=this;this.showLastMsg=!0,setTimeout((function(){t.showLastMsg=!1}),3e3)},prices:function(e){if(3==e.length){var t="https://i.gifer.com/7VzX.gif";this.postGif(t)}if(5==e.length&&this.say("Diamond hands 💎🤲: \nHolding strong for ".concat(e.length*this.tickFrequency," seconds already!")),8==e.length){var n="https://c.tenor.com/puvU5YS9r4cAAAAC/uncle-scrooge-mcduck-money.gif";this.postGif(n)}if(10==e.length&&this.say("To the moon 🚀: \nStock is going up for ".concat(e.length*this.tickFrequency," seconds.")),13==e.length){var a="https://c.tenor.com/QfVo3Mh29hUAAAAC/we-bare-bears-money.gif";this.postGif(a)}if(15==e.length&&this.say("Gimme the tendies! 🍗: \nCash piling up for ".concat(e.length*this.tickFrequency," seconds now.")),18==e.length){var r="https://c.tenor.com/0-e7d7ct3G0AAAAC/shut-up-and-take-my-money-futurama.gif";this.postGif(r)}if(20==e.length&&this.say("Almost there 🚀🚀🚀🚀: \nImpressive run for ".concat(e.length*this.tickFrequency," seconds.")),22==e.length){var i="https://slack-imgs.com/?c=1&o1=ro&url=https%3A%2F%2Ftenor.com%2Fview%2Fbacking-you-get-yours-danny-devito-danny-devito-gif-13052176";this.postGif(i)}e.length>=te&&(this.submittable=!0)},submittable:function(e){var t=this;return Object(o["a"])(regeneratorRuntime.mark((function n(){return regeneratorRuntime.wrap((function(n){while(1)switch(n.prev=n.next){case 0:if(!e){n.next=5;break}return n.next=3,t.sendMessage({name:"Trade_ends"});case 3:t.showEndDialog=!0,t.onPause=!0;case 5:case"end":return n.stop()}}),n)})))()},currentPrice:function(e){this.$refs.listend&&this.$refs.listend.scrollIntoView({behavior:"smooth"}),q["a"].to(this.$data,{duration:.5,tweenedPrice:e,onUpdate:this.tweenUpd})}},created:function(){var e=this;return Object(o["a"])(regeneratorRuntime.mark((function t(){return regeneratorRuntime.wrap((function(t){while(1)switch(t.prev=t.next){case 0:e.$options.sockets.onopen=Object(o["a"])(regeneratorRuntime.mark((function t(){return regeneratorRuntime.wrap((function(t){while(1)switch(t.prev=t.next){case 0:return t.next=2,e.sendMessage({name:"Trade_starts"});case 2:return t.abrupt("return",t.sent);case 3:case"end":return t.stop()}}),t)}))),e.$options.sockets.onmessage=function(e){return console.log(e)};case 2:case"end":return t.stop()}}),t)})))()},mounted:function(){var e=this;return Object(o["a"])(regeneratorRuntime.mark((function t(){return regeneratorRuntime.wrap((function(t){while(1)switch(t.prev=t.next){case 0:e.say("Hello! Ready to invest with me? 📈 "),e.$nextTick((function(){e.$refs.listend&&e.$refs.listend.scrollIntoView({behavior:"smooth"}),e.$refs.priceGraph.chart.setSize(null,window.innerHeight-100)})),e.stockInterval=setInterval(Object(o["a"])(regeneratorRuntime.mark((function t(){var n,a;return regeneratorRuntime.wrap((function(t){while(1)switch(t.prev=t.next){case 0:e.onPause||(e.timeInTrade+=e.tickFrequency,n=ee.a.random(0,2),e.currentPrice+=n,e.counter++,a=ee.a.random(0,1,!0),a<e.probToZero&&(e.submittable=!0,e.currentPrice=0),e.addMessage(e.currentPrice,n),e.prices.push(e.currentPrice),e.chartOptions.series[0].data.push([Object(B["a"])(new Date),e.currentPrice]));case 1:case"end":return t.stop()}}),t)}))),1e3*e.tickFrequency);case 3:case"end":return t.stop()}}),t)})))()},methods:{showInstructions:function(){},postGif:function(e){var t='<img src="'.concat(e,'" width="180px"/>');this.messages.push(t)},say:function(e){var t=this;this.currentMessage=e,setTimeout((function(){t.currentMessage=null,t.messages.push(e)}),this.messageMoveDelay)},locked:function(e){var t=this.awardsGiven.includes(e);return!t},classAward:function(e){return this.locked(e)?"gray":""},finishGame:function(){var e=this;return Object(o["a"])(regeneratorRuntime.mark((function t(){return regeneratorRuntime.wrap((function(t){while(1)switch(t.prev=t.next){case 0:return t.next=2,e.sendMessage({name:"round_ends"});case 2:document.getElementById("form").submit();case 3:case"end":return t.stop()}}),t)})))()},addMessage:function(e,t){if(0===e){var n="Market crashed! 😢";this.say(n)}0!==t||this.onPause||(this.zeroCounter++,this.TwoTwosCounter=0,this.grownCounter=0),t>0&&!this.onPause&&(this.zeroCounter=0,this.grownCounter++,2==t&&this.TwoTwosCounter++)},sendMessage:function(e){var t=this;return Object(o["a"])(regeneratorRuntime.mark((function n(){var a;return regeneratorRuntime.wrap((function(n){while(1)switch(n.prev=n.next){case 0:if(1!=t.$socket.readyState){n.next=4;break}return a={currentPrice:t.currentPrice,priceIndex:t.counter,secs_since_round_starts:Object(Y["a"])(new Date,t.startTime)},n.next=4,t.$socket.sendObj(Object(s["a"])(Object(s["a"])({},e),a));case 4:case"end":return n.stop()}}),n)})))()},tweenUpd:function(e){this.tweenedPrice=ee.a.round(this.tweenedPrice,2)},sell:function(){var e=this;return Object(o["a"])(regeneratorRuntime.mark((function t(){return regeneratorRuntime.wrap((function(t){while(1)switch(t.prev=t.next){case 0:return t.next=2,e.sendMessage({name:"Sell"});case 2:e.dialog=!1,e.submittable=!0,e.onPause=!0;case 5:case"end":return t.stop()}}),t)})))()},showSellingDialog:function(){var e=this;return Object(o["a"])(regeneratorRuntime.mark((function t(){return regeneratorRuntime.wrap((function(t){while(1)switch(t.prev=t.next){case 0:return t.next=2,e.sendMessage({name:"sellingDialogShown"});case 2:e.dialog=!0;case 3:case"end":return t.stop()}}),t)})))()},continueKeeping:function(){var e=this;return Object(o["a"])(regeneratorRuntime.mark((function t(){return regeneratorRuntime.wrap((function(t){while(1)switch(t.prev=t.next){case 0:return t.next=2,e.sendMessage({name:"continueKeeping"});case 2:e.dialog=!1,e.submittable=!1,e.showHappyFace=!0,setTimeout((function(){e.showHappyFace=!1,e.onPause=False}),3e3);case 6:case"end":return t.stop()}}),t)})))()}}},ie=re,se=(n("034f"),n("7496")),oe=n("40dc"),ce=n("8212"),le=n("4ca6"),ue=n("62ad"),de=n("a523"),ge=n("132d"),pe=n("adda"),me=n("8860"),ve=n("da13"),fe=n("5d23"),he=n("1baa"),be=n("f6c4"),we=n("f774"),Ae=n("a797"),Ce=n("0fd9"),xe=n("2db4"),Ie=n("afd9"),ye=n("3a2f"),ke=Object(f["a"])(ie,r,i,!1,null,null,null),Pe=ke.exports;y()(ke,{VApp:se["a"],VAppBar:oe["a"],VAvatar:ce["a"],VBadge:le["a"],VBtn:k["a"],VCard:P["a"],VCardText:V["b"],VCardTitle:V["c"],VCol:ue["a"],VContainer:de["a"],VIcon:ge["a"],VImg:pe["a"],VList:me["a"],VListItem:ve["a"],VListItemContent:fe["a"],VListItemGroup:he["a"],VListItemTitle:fe["b"],VMain:be["a"],VNavigationDrawer:we["a"],VOverlay:Ae["a"],VRow:Ce["a"],VSheet:G["a"],VSnackbar:xe["a"],VSpacer:j["a"],VSystemBar:Ie["a"],VTooltip:ye["a"]});var Ve=n("f309");a["default"].use(Ve["a"]);var Re=new Ve["a"]({icons:{iconfont:"mdi"}}),Ge=n("ea7f"),je=n.n(Ge),Te=n("37d8"),Oe=n.n(Te),_e=n("b408"),Se=n.n(_e),De=n("467a"),Le=(n("77ed"),n("bf40"),n("2f62"));a["default"].use(Le["a"]);var Me=new Le["a"].Store({state:{},mutations:{},actions:{}});a["default"].use(De["a"]),a["default"].prototype.$gamified=window.gamified,a["default"].use(l["b"]);var We="https:"===window.location.protocol?"wss":"ws",Ee=We+"://"+window.location.host+window.socket_path;console.debug("WASPATH",Ee),a["default"].use(Se.a,Ee,{format:"json",reconnection:!0,reconnectionAttempts:5,reconnectionDelay:3e3}),Oe()(je.a),a["default"].use(N.a),a["default"].config.productionTip=!1,new a["default"]({vuetify:Re,store:Me,render:function(e){return e(Pe)}}).$mount("#app")},"6b01":function(e,t,n){},"85ec":function(e,t,n){},f5da:function(e,t,n){"use strict";n("6b01")}});