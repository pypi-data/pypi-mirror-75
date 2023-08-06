(self.webpackJsonp=self.webpackJsonp||[]).push([[125],{114:function(e,t,i){"use strict";i.d(t,"a",(function(){return s})),i.d(t,"b",(function(){return o})),i.d(t,"d",(function(){return c})),i.d(t,"g",(function(){return l})),i.d(t,"h",(function(){return d})),i.d(t,"c",(function(){return h})),i.d(t,"e",(function(){return u})),i.d(t,"f",(function(){return m})),i.d(t,"j",(function(){return g})),i.d(t,"i",(function(){return b}));var a=i(19),n=i(64),r=i(127);const s=["unignore","homekit","ssdp","zeroconf","discovery"],o=(e,t)=>{var i;return e.callApi("POST","config/config_entries/flow",{handler:t,show_advanced_options:Boolean(null===(i=e.userData)||void 0===i?void 0:i.showAdvanced)})},c=(e,t)=>e.callApi("GET","config/config_entries/flow/"+t),l=(e,t,i)=>e.callApi("POST","config/config_entries/flow/"+t,i),d=(e,t)=>e.callWS({type:"config_entries/ignore_flow",flow_id:t}),h=(e,t)=>e.callApi("DELETE","config/config_entries/flow/"+t),u=e=>e.callApi("GET","config/config_entries/flow_handlers"),p=e=>e.sendMessagePromise({type:"config_entries/flow/progress"}),f=(e,t)=>e.subscribeEvents(Object(n.a)(()=>p(e).then(e=>t.setState(e,!0)),500,!0),"config_entry_discovered"),m=e=>Object(a.b)(e,"_configFlowProgress",p,f),g=(e,t)=>m(e.connection).subscribe(t),b=(e,t)=>{const i=t.context.title_placeholders||{},a=Object.keys(i);if(0===a.length)return Object(r.a)(e,t.handler);const n=[];return a.forEach(e=>{n.push(e),n.push(i[e])}),e(`component.${t.handler}.config.flow_title`,...n)}},127:function(e,t,i){"use strict";i.d(t,"d",(function(){return a})),i.d(t,"a",(function(){return n})),i.d(t,"c",(function(){return r})),i.d(t,"b",(function(){return s}));const a=(e,t)=>t.issue_tracker||`https://github.com/home-assistant/home-assistant/issues?q=is%3Aissue+is%3Aopen+label%3A%22integration%3A+${e}%22`,n=(e,t)=>e(`component.${t}.title`)||t,r=e=>e.callWS({type:"manifest/list"}),s=(e,t)=>e.callWS({type:"manifest/get",integration:t})},151:function(e,t,i){"use strict";i.d(t,"a",(function(){return n})),i.d(t,"b",(function(){return r}));var a=i(12);const n=()=>Promise.all([i.e(1),i.e(0),i.e(2),i.e(3),i.e(52)]).then(i.bind(null,208)),r=(e,t,i)=>{Object(a.a)(e,"show-dialog",{dialogTag:"dialog-data-entry-flow",dialogImport:n,dialogParams:{...t,flowConfig:i}})}},159:function(e,t,i){"use strict";i.d(t,"b",(function(){return a})),i.d(t,"a",(function(){return n}));const a=(e,t)=>e<t?-1:e>t?1:0,n=(e,t)=>a(e.toLowerCase(),t.toLowerCase())},174:function(e,t,i){"use strict";i.d(t,"a",(function(){return l})),i.d(t,"b",(function(){return d}));var a=i(0),n=i(159),r=i(56),s=i(114),o=i(127),c=i(151);const l=c.a,d=(e,t)=>Object(c.b)(e,t,{loadDevicesAndAreas:!0,getFlowHandlers:async e=>{const[t]=await Promise.all([Object(s.e)(e),e.loadBackendTranslation("title",void 0,!0)]);return t.sort((t,i)=>Object(n.a)(Object(o.a)(e.localize,t),Object(o.a)(e.localize,i)))},createFlow:async(e,t)=>{const[i]=await Promise.all([Object(s.b)(e,t),e.loadBackendTranslation("config",t)]);return i},fetchFlow:async(e,t)=>{const i=await Object(s.d)(e,t);return await e.loadBackendTranslation("config",i.handler),i},handleFlowStep:s.g,deleteFlow:s.c,renderAbortDescription(e,t){const i=Object(r.b)(e.localize,`component.${t.handler}.config.abort.${t.reason}`,t.description_placeholders);return i?a.f`
            <ha-markdown allowsvg breaks .content=${i}></ha-markdown>
          `:""},renderShowFormStepHeader:(e,t)=>e.localize(`component.${t.handler}.config.step.${t.step_id}.title`)||e.localize(`component.${t.handler}.title`),renderShowFormStepDescription(e,t){const i=Object(r.b)(e.localize,`component.${t.handler}.config.step.${t.step_id}.description`,t.description_placeholders);return i?a.f`
            <ha-markdown allowsvg breaks .content=${i}></ha-markdown>
          `:""},renderShowFormStepFieldLabel:(e,t,i)=>e.localize(`component.${t.handler}.config.step.${t.step_id}.data.${i.name}`),renderShowFormStepFieldError:(e,t,i)=>e.localize(`component.${t.handler}.config.error.${i}`),renderExternalStepHeader:(e,t)=>e.localize(`component.${t.handler}.config.step.${t.step_id}.title`),renderExternalStepDescription(e,t){const i=Object(r.b)(e.localize,`component.${t.handler}.config.${t.step_id}.description`,t.description_placeholders);return a.f`
        <p>
          ${e.localize("ui.panel.config.integrations.config_flow.external_step.description")}
        </p>
        ${i?a.f`
              <ha-markdown
                allowsvg
                breaks
                .content=${i}
              ></ha-markdown>
            `:""}
      `},renderCreateEntryDescription(e,t){const i=Object(r.b)(e.localize,`component.${t.handler}.config.create_entry.${t.description||"default"}`,t.description_placeholders);return a.f`
        ${i?a.f`
              <ha-markdown
                allowsvg
                breaks
                .content=${i}
              ></ha-markdown>
            `:""}
        <p>
          ${e.localize("ui.panel.config.integrations.config_flow.created_config","name",t.title)}
        </p>
      `}})},184:function(e,t,i){"use strict";i(143);var a=i(0);i(139);function n(e){var t,i=l(e.key);"method"===e.kind?t={value:e.value,writable:!0,configurable:!0,enumerable:!1}:"get"===e.kind?t={get:e.value,configurable:!0,enumerable:!1}:"set"===e.kind?t={set:e.value,configurable:!0,enumerable:!1}:"field"===e.kind&&(t={configurable:!0,writable:!0,enumerable:!0});var a={kind:"field"===e.kind?"field":"method",key:i,placement:e.static?"static":"field"===e.kind?"own":"prototype",descriptor:t};return e.decorators&&(a.decorators=e.decorators),"field"===e.kind&&(a.initializer=e.value),a}function r(e,t){void 0!==e.descriptor.get?t.descriptor.get=e.descriptor.get:t.descriptor.set=e.descriptor.set}function s(e){return e.decorators&&e.decorators.length}function o(e){return void 0!==e&&!(void 0===e.value&&void 0===e.writable)}function c(e,t){var i=e[t];if(void 0!==i&&"function"!=typeof i)throw new TypeError("Expected '"+t+"' to be a function");return i}function l(e){var t=function(e,t){if("object"!=typeof e||null===e)return e;var i=e[Symbol.toPrimitive];if(void 0!==i){var a=i.call(e,t||"default");if("object"!=typeof a)return a;throw new TypeError("@@toPrimitive must return a primitive value.")}return("string"===t?String:Number)(e)}(e,"string");return"symbol"==typeof t?t:String(t)}function d(e,t){(null==t||t>e.length)&&(t=e.length);for(var i=0,a=new Array(t);i<t;i++)a[i]=e[i];return a}!function(e,t,i,a){var h=function(){(function(){return e});var e={elementsDefinitionOrder:[["method"],["field"]],initializeInstanceElements:function(e,t){["method","field"].forEach((function(i){t.forEach((function(t){t.kind===i&&"own"===t.placement&&this.defineClassElement(e,t)}),this)}),this)},initializeClassElements:function(e,t){var i=e.prototype;["method","field"].forEach((function(a){t.forEach((function(t){var n=t.placement;if(t.kind===a&&("static"===n||"prototype"===n)){var r="static"===n?e:i;this.defineClassElement(r,t)}}),this)}),this)},defineClassElement:function(e,t){var i=t.descriptor;if("field"===t.kind){var a=t.initializer;i={enumerable:i.enumerable,writable:i.writable,configurable:i.configurable,value:void 0===a?void 0:a.call(e)}}Object.defineProperty(e,t.key,i)},decorateClass:function(e,t){var i=[],a=[],n={static:[],prototype:[],own:[]};if(e.forEach((function(e){this.addElementPlacement(e,n)}),this),e.forEach((function(e){if(!s(e))return i.push(e);var t=this.decorateElement(e,n);i.push(t.element),i.push.apply(i,t.extras),a.push.apply(a,t.finishers)}),this),!t)return{elements:i,finishers:a};var r=this.decorateConstructor(i,t);return a.push.apply(a,r.finishers),r.finishers=a,r},addElementPlacement:function(e,t,i){var a=t[e.placement];if(!i&&-1!==a.indexOf(e.key))throw new TypeError("Duplicated element ("+e.key+")");a.push(e.key)},decorateElement:function(e,t){for(var i=[],a=[],n=e.decorators,r=n.length-1;r>=0;r--){var s=t[e.placement];s.splice(s.indexOf(e.key),1);var o=this.fromElementDescriptor(e),c=this.toElementFinisherExtras((0,n[r])(o)||o);e=c.element,this.addElementPlacement(e,t),c.finisher&&a.push(c.finisher);var l=c.extras;if(l){for(var d=0;d<l.length;d++)this.addElementPlacement(l[d],t);i.push.apply(i,l)}}return{element:e,finishers:a,extras:i}},decorateConstructor:function(e,t){for(var i=[],a=t.length-1;a>=0;a--){var n=this.fromClassDescriptor(e),r=this.toClassDescriptor((0,t[a])(n)||n);if(void 0!==r.finisher&&i.push(r.finisher),void 0!==r.elements){e=r.elements;for(var s=0;s<e.length-1;s++)for(var o=s+1;o<e.length;o++)if(e[s].key===e[o].key&&e[s].placement===e[o].placement)throw new TypeError("Duplicated element ("+e[s].key+")")}}return{elements:e,finishers:i}},fromElementDescriptor:function(e){var t={kind:e.kind,key:e.key,placement:e.placement,descriptor:e.descriptor};return Object.defineProperty(t,Symbol.toStringTag,{value:"Descriptor",configurable:!0}),"field"===e.kind&&(t.initializer=e.initializer),t},toElementDescriptors:function(e){var t;if(void 0!==e)return(t=e,function(e){if(Array.isArray(e))return e}(t)||function(e){if("undefined"!=typeof Symbol&&Symbol.iterator in Object(e))return Array.from(e)}(t)||function(e,t){if(e){if("string"==typeof e)return d(e,t);var i=Object.prototype.toString.call(e).slice(8,-1);return"Object"===i&&e.constructor&&(i=e.constructor.name),"Map"===i||"Set"===i?Array.from(i):"Arguments"===i||/^(?:Ui|I)nt(?:8|16|32)(?:Clamped)?Array$/.test(i)?d(e,t):void 0}}(t)||function(){throw new TypeError("Invalid attempt to destructure non-iterable instance.\nIn order to be iterable, non-array objects must have a [Symbol.iterator]() method.")}()).map((function(e){var t=this.toElementDescriptor(e);return this.disallowProperty(e,"finisher","An element descriptor"),this.disallowProperty(e,"extras","An element descriptor"),t}),this)},toElementDescriptor:function(e){var t=String(e.kind);if("method"!==t&&"field"!==t)throw new TypeError('An element descriptor\'s .kind property must be either "method" or "field", but a decorator created an element descriptor with .kind "'+t+'"');var i=l(e.key),a=String(e.placement);if("static"!==a&&"prototype"!==a&&"own"!==a)throw new TypeError('An element descriptor\'s .placement property must be one of "static", "prototype" or "own", but a decorator created an element descriptor with .placement "'+a+'"');var n=e.descriptor;this.disallowProperty(e,"elements","An element descriptor");var r={kind:t,key:i,placement:a,descriptor:Object.assign({},n)};return"field"!==t?this.disallowProperty(e,"initializer","A method descriptor"):(this.disallowProperty(n,"get","The property descriptor of a field descriptor"),this.disallowProperty(n,"set","The property descriptor of a field descriptor"),this.disallowProperty(n,"value","The property descriptor of a field descriptor"),r.initializer=e.initializer),r},toElementFinisherExtras:function(e){return{element:this.toElementDescriptor(e),finisher:c(e,"finisher"),extras:this.toElementDescriptors(e.extras)}},fromClassDescriptor:function(e){var t={kind:"class",elements:e.map(this.fromElementDescriptor,this)};return Object.defineProperty(t,Symbol.toStringTag,{value:"Descriptor",configurable:!0}),t},toClassDescriptor:function(e){var t=String(e.kind);if("class"!==t)throw new TypeError('A class descriptor\'s .kind property must be "class", but a decorator created a class descriptor with .kind "'+t+'"');this.disallowProperty(e,"key","A class descriptor"),this.disallowProperty(e,"placement","A class descriptor"),this.disallowProperty(e,"descriptor","A class descriptor"),this.disallowProperty(e,"initializer","A class descriptor"),this.disallowProperty(e,"extras","A class descriptor");var i=c(e,"finisher");return{elements:this.toElementDescriptors(e.elements),finisher:i}},runClassFinishers:function(e,t){for(var i=0;i<t.length;i++){var a=(0,t[i])(e);if(void 0!==a){if("function"!=typeof a)throw new TypeError("Finishers must return a constructor.");e=a}}return e},disallowProperty:function(e,t,i){if(void 0!==e[t])throw new TypeError(i+" can't have a ."+t+" property.")}};return e}();if(a)for(var u=0;u<a.length;u++)h=a[u](h);var p=t((function(e){h.initializeInstanceElements(e,f.elements)}),i),f=h.decorateClass(function(e){for(var t=[],i=function(e){return"method"===e.kind&&e.key===c.key&&e.placement===c.placement},a=0;a<e.length;a++){var n,c=e[a];if("method"===c.kind&&(n=t.find(i)))if(o(c.descriptor)||o(n.descriptor)){if(s(c)||s(n))throw new ReferenceError("Duplicated methods ("+c.key+") can't be decorated.");n.descriptor=c.descriptor}else{if(s(c)){if(s(n))throw new ReferenceError("Decorators can't be placed on different accessors with for the same property ("+c.key+").");n.decorators=c.decorators}r(c,n)}else t.push(c)}return t}(p.d.map(n)),e);h.initializeClassElements(p.F,f.elements),h.runClassFinishers(p.F,f.finishers)}([Object(a.d)("ha-icon-button")],(function(e,t){return{F:class extends t{constructor(...t){super(...t),e(this)}},d:[{kind:"field",decorators:[Object(a.h)({type:Boolean,reflect:!0})],key:"disabled",value:()=>!1},{kind:"field",decorators:[Object(a.h)({type:String})],key:"icon",value:()=>""},{kind:"field",decorators:[Object(a.h)({type:String})],key:"label",value:()=>""},{kind:"method",key:"createRenderRoot",value:function(){return this.attachShadow({mode:"open",delegatesFocus:!0})}},{kind:"method",key:"render",value:function(){return a.f`
      <mwc-icon-button .label=${this.label} .disabled=${this.disabled}>
        <ha-icon .icon=${this.icon}></ha-icon>
      </mwc-icon-button>
    `}},{kind:"get",static:!0,key:"styles",value:function(){return a.c`
      :host {
        display: inline-block;
        outline: none;
      }
      :host([disabled]) {
        pointer-events: none;
      }
      mwc-icon-button {
        --mdc-theme-on-primary: currentColor;
        --mdc-theme-text-disabled-on-light: var(--disabled-text-color);
      }
      ha-icon {
        --ha-icon-display: inline;
      }
    `}}]}}),a.a)},215:function(e,t,i){"use strict";var a=i(9);t.a=Object(a.a)(e=>class extends e{static get properties(){return{hass:Object,localize:{type:Function,computed:"__computeLocalize(hass.localize)"}}}__computeLocalize(e){return e}})},239:function(e,t,i){"use strict";i.d(t,"a",(function(){return a})),i.d(t,"c",(function(){return n})),i.d(t,"b",(function(){return r}));const a=function(){try{(new Date).toLocaleDateString("i")}catch(e){return"RangeError"===e.name}return!1}(),n=function(){try{(new Date).toLocaleTimeString("i")}catch(e){return"RangeError"===e.name}return!1}(),r=function(){try{(new Date).toLocaleString("i")}catch(e){return"RangeError"===e.name}return!1}()},241:function(e,t,i){"use strict";i.d(t,"a",(function(){return r})),i.d(t,"b",(function(){return s}));var a=i(240),n=i(239);const r=n.b?(e,t)=>e.toLocaleString(t,{year:"numeric",month:"long",day:"numeric",hour:"numeric",minute:"2-digit"}):e=>Object(a.a)(e,"MMMM D, YYYY, HH:mm"),s=n.b?(e,t)=>e.toLocaleString(t,{year:"numeric",month:"long",day:"numeric",hour:"numeric",minute:"2-digit",second:"2-digit"}):e=>Object(a.a)(e,"MMMM D, YYYY, HH:mm:ss")},269:function(e,t,i){"use strict";i.d(t,"a",(function(){return r})),i.d(t,"b",(function(){return s}));var a=i(240),n=i(239);const r=n.c?(e,t)=>e.toLocaleTimeString(t,{hour:"numeric",minute:"2-digit"}):e=>Object(a.a)(e,"shortTime"),s=n.c?(e,t)=>e.toLocaleTimeString(t,{hour:"numeric",minute:"2-digit",second:"2-digit"}):e=>Object(a.a)(e,"mediumTime")},277:function(e,t,i){"use strict";i.d(t,"b",(function(){return n})),i.d(t,"a",(function(){return r}));const a=/^(\w+)\.(\w+)$/,n=e=>a.test(e),r=e=>e.toLowerCase().replace(/\s|'|\./g,"_").replace(/\W/g,"").replace(/_{2,}/g,"_").replace(/_$/,"")},287:function(e,t,i){"use strict";i.d(t,"a",(function(){return n}));var a=i(277);const n=e=>{if(!e||!Array.isArray(e))throw new Error("Entities need to be an array");return e.map((e,t)=>{if("object"==typeof e&&!Array.isArray(e)&&e.type)return e;let i;if("string"==typeof e)i={entity:e};else{if("object"!=typeof e||Array.isArray(e))throw new Error(`Invalid entity specified at position ${t}.`);if(!e.entity)throw new Error(`Entity object at position ${t} is missing entity field.`);i=e}if(!Object(a.b)(i.entity))throw new Error(`Invalid entity ID at position ${t}: ${i.entity}`);return i})}},346:function(e,t,i){"use strict";i(160);var a=i(4),n=i(32),r=i(215),s=i(22),o=i(241),c=i(130),l=(i(184),i(92)),d=i(13),h=i(269);let u=null;class p extends(Object(l.b)([c.a],n.a)){static get template(){return a.a`
      <style>
        :host {
          display: block;
        }
        .chartHeader {
          padding: 6px 0 0 0;
          width: 100%;
          display: flex;
          flex-direction: row;
        }
        .chartHeader > div {
          vertical-align: top;
          padding: 0 8px;
        }
        .chartHeader > div.chartTitle {
          padding-top: 8px;
          flex: 0 0 0;
          max-width: 30%;
        }
        .chartHeader > div.chartLegend {
          flex: 1 1;
          min-width: 70%;
        }
        :root {
          user-select: none;
          -moz-user-select: none;
          -webkit-user-select: none;
          -ms-user-select: none;
        }
        .chartTooltip {
          font-size: 90%;
          opacity: 1;
          position: absolute;
          background: rgba(80, 80, 80, 0.9);
          color: white;
          border-radius: 3px;
          pointer-events: none;
          transform: translate(-50%, 12px);
          z-index: 1000;
          width: 200px;
          transition: opacity 0.15s ease-in-out;
        }
        :host([rtl]) .chartTooltip {
          direction: rtl;
        }
        .chartLegend ul,
        .chartTooltip ul {
          display: inline-block;
          padding: 0 0px;
          margin: 5px 0 0 0;
          width: 100%;
        }
        .chartTooltip li {
          display: block;
          white-space: pre-line;
        }
        .chartTooltip .title {
          text-align: center;
          font-weight: 500;
        }
        .chartLegend li {
          display: inline-block;
          padding: 0 6px;
          max-width: 49%;
          text-overflow: ellipsis;
          white-space: nowrap;
          overflow: hidden;
          box-sizing: border-box;
        }
        .chartLegend li:nth-child(odd):last-of-type {
          /* Make last item take full width if it is odd-numbered. */
          max-width: 100%;
        }
        .chartLegend li[data-hidden] {
          text-decoration: line-through;
        }
        .chartLegend em,
        .chartTooltip em {
          border-radius: 5px;
          display: inline-block;
          height: 10px;
          margin-right: 4px;
          width: 10px;
        }
        :host([rtl]) .chartTooltip em {
          margin-right: inherit;
          margin-left: 4px;
        }
        ha-icon-button {
          color: var(--secondary-text-color);
        }
      </style>
      <template is="dom-if" if="[[unit]]">
        <div class="chartHeader">
          <div class="chartTitle">[[unit]]</div>
          <div class="chartLegend">
            <ul>
              <template is="dom-repeat" items="[[metas]]">
                <li on-click="_legendClick" data-hidden$="[[item.hidden]]">
                  <em style$="background-color:[[item.bgColor]]"></em>
                  [[item.label]]
                </li>
              </template>
            </ul>
          </div>
        </div>
      </template>
      <div id="chartTarget" style="height:40px; width:100%">
        <canvas id="chartCanvas"></canvas>
        <div
          class$="chartTooltip [[tooltip.yAlign]]"
          style$="opacity:[[tooltip.opacity]]; top:[[tooltip.top]]; left:[[tooltip.left]]; padding:[[tooltip.yPadding]]px [[tooltip.xPadding]]px"
        >
          <div class="title">[[tooltip.title]]</div>
          <div>
            <ul>
              <template is="dom-repeat" items="[[tooltip.lines]]">
                <li>
                  <em style$="background-color:[[item.bgColor]]"></em
                  >[[item.text]]
                </li>
              </template>
            </ul>
          </div>
        </div>
      </div>
    `}get chart(){return this._chart}static get properties(){return{data:Object,identifier:String,rendered:{type:Boolean,notify:!0,value:!1,readOnly:!0},metas:{type:Array,value:()=>[]},tooltip:{type:Object,value:()=>({opacity:"0",left:"0",top:"0",xPadding:"5",yPadding:"3"})},unit:Object,rtl:{type:Boolean,reflectToAttribute:!0}}}static get observers(){return["onPropsChange(data)"]}connectedCallback(){super.connectedCallback(),this._isAttached=!0,this.onPropsChange(),this._resizeListener=()=>{this._debouncer=s.a.debounce(this._debouncer,d.d.after(10),()=>{this._isAttached&&this.resizeChart()})},"function"==typeof ResizeObserver?(this.resizeObserver=new ResizeObserver(e=>{e.forEach(()=>{this._resizeListener()})}),this.resizeObserver.observe(this.$.chartTarget)):this.addEventListener("iron-resize",this._resizeListener),null===u&&(u=Promise.all([i.e(187),i.e(99)]).then(i.bind(null,803))),u.then(e=>{this.ChartClass=e.default,this.onPropsChange()})}disconnectedCallback(){super.disconnectedCallback(),this._isAttached=!1,this.resizeObserver&&this.resizeObserver.unobserve(this.$.chartTarget),this.removeEventListener("iron-resize",this._resizeListener),void 0!==this._resizeTimer&&(clearInterval(this._resizeTimer),this._resizeTimer=void 0)}onPropsChange(){this._isAttached&&this.ChartClass&&this.data&&this.drawChart()}_customTooltips(e){if(0===e.opacity)return void this.set(["tooltip","opacity"],0);e.yAlign?this.set(["tooltip","yAlign"],e.yAlign):this.set(["tooltip","yAlign"],"no-transform");const t=e.title&&e.title[0]||"";this.set(["tooltip","title"],t);const i=e.body.map(e=>e.lines);e.body&&this.set(["tooltip","lines"],i.map((t,i)=>{const a=e.labelColors[i];return{color:a.borderColor,bgColor:a.backgroundColor,text:t.join("\n")}}));const a=this.$.chartTarget.clientWidth;let n=e.caretX;const r=this._chart.canvas.offsetTop+e.caretY;e.caretX+100>a?n=a-100:e.caretX<100&&(n=100),n+=this._chart.canvas.offsetLeft,this.tooltip={...this.tooltip,opacity:1,left:n+"px",top:r+"px"}}_legendClick(e){(e=e||window.event).stopPropagation();let t=e.target||e.srcElement;for(;"LI"!==t.nodeName;)t=t.parentElement;const i=e.model.itemsIndex,a=this._chart.getDatasetMeta(i);a.hidden=null===a.hidden?!this._chart.data.datasets[i].hidden:null,this.set(["metas",i,"hidden"],this._chart.isDatasetVisible(i)?null:"hidden"),this._chart.update()}_drawLegend(){const e=this._chart,t=this._oldIdentifier&&this.identifier===this._oldIdentifier;this._oldIdentifier=this.identifier,this.set("metas",this._chart.data.datasets.map((i,a)=>({label:i.label,color:i.color,bgColor:i.backgroundColor,hidden:t&&a<this.metas.length?this.metas[a].hidden:!e.isDatasetVisible(a)})));let i=!1;if(t)for(let a=0;a<this.metas.length;a++){const t=e.getDatasetMeta(a);!!t.hidden!=!!this.metas[a].hidden&&(i=!0),t.hidden=!!this.metas[a].hidden||null}i&&e.update(),this.unit=this.data.unit}_formatTickValue(e,t,i){if(0===i.length)return e;const a=new Date(i[t].value);return Object(h.a)(a)}drawChart(){const e=this.data.data,t=this.$.chartCanvas;if(e.datasets&&e.datasets.length||this._chart){if("timeline"!==this.data.type&&e.datasets.length>0){const t=e.datasets.length,i=this.constructor.getColorList(t);for(let a=0;a<t;a++)e.datasets[a].borderColor=i[a].rgbString(),e.datasets[a].backgroundColor=i[a].alpha(.6).rgbaString()}if(this._chart)this._customTooltips({opacity:0}),this._chart.data=e,this._chart.update({duration:0}),this.isTimeline?this._chart.options.scales.yAxes[0].gridLines.display=e.length>1:!0===this.data.legend&&this._drawLegend(),this.resizeChart();else{if(!e.datasets)return;this._customTooltips({opacity:0});const i=[{afterRender:()=>this._setRendered(!0)}];let a={responsive:!0,maintainAspectRatio:!1,animation:{duration:0},hover:{animationDuration:0},responsiveAnimationDuration:0,tooltips:{enabled:!1,custom:this._customTooltips.bind(this)},legend:{display:!1},line:{spanGaps:!0},elements:{font:"12px 'Roboto', 'sans-serif'"},ticks:{fontFamily:"'Roboto', 'sans-serif'"}};a=Chart.helpers.merge(a,this.data.options),a.scales.xAxes[0].ticks.callback=this._formatTickValue,"timeline"===this.data.type?(this.set("isTimeline",!0),void 0!==this.data.colors&&(this._colorFunc=this.constructor.getColorGenerator(this.data.colors.staticColors,this.data.colors.staticColorIndex)),void 0!==this._colorFunc&&(a.elements.colorFunction=this._colorFunc),1===e.datasets.length&&(a.scales.yAxes[0].ticks?a.scales.yAxes[0].ticks.display=!1:a.scales.yAxes[0].ticks={display:!1},a.scales.yAxes[0].gridLines?a.scales.yAxes[0].gridLines.display=!1:a.scales.yAxes[0].gridLines={display:!1}),this.$.chartTarget.style.height="50px"):this.$.chartTarget.style.height="160px";const n={type:this.data.type,data:this.data.data,options:a,plugins:i};this._chart=new this.ChartClass(t,n),!0!==this.isTimeline&&!0===this.data.legend&&this._drawLegend(),this.resizeChart()}}}resizeChart(){this._chart&&(void 0!==this._resizeTimer?(clearInterval(this._resizeTimer),this._resizeTimer=void 0,this._resizeChart()):this._resizeTimer=setInterval(this.resizeChart.bind(this),10))}_resizeChart(){const e=this.$.chartTarget,t=this.data.data;if(0===t.datasets.length)return;if(!this.isTimeline)return void this._chart.resize();const i=this._chart.chartArea.top,a=this._chart.chartArea.bottom,n=this._chart.canvas.clientHeight;if(a>0&&(this._axisHeight=n-a+i),!this._axisHeight)return e.style.height="50px",this._chart.resize(),void this.resizeChart();if(this._axisHeight){const i=30*t.datasets.length+this._axisHeight+"px";e.style.height!==i&&(e.style.height=i),this._chart.resize()}}static getColorList(e){let t=!1;e>10&&(t=!0,e=Math.ceil(e/2));const i=360/e,a=[];for(let n=0;n<e;n++)a[n]=Color().hsl(i*n,80,38),t&&(a[n+e]=Color().hsl(i*n,80,62));return a}static getColorGenerator(e,t){const i=["ff0029","66a61e","377eb8","984ea3","00d2d5","ff7f00","af8d00","7f80cd","b3e900","c42e60","a65628","f781bf","8dd3c7","bebada","fb8072","80b1d3","fdb462","fccde5","bc80bd","ffed6f","c4eaff","cf8c00","1b9e77","d95f02","e7298a","e6ab02","a6761d","0097ff","00d067","f43600","4ba93b","5779bb","927acc","97ee3f","bf3947","9f5b00","f48758","8caed6","f2b94f","eff26e","e43872","d9b100","9d7a00","698cff","d9d9d9","00d27e","d06800","009f82","c49200","cbe8ff","fecddf","c27eb6","8cd2ce","c4b8d9","f883b0","a49100","f48800","27d0df","a04a9b"];function a(e){return Color("#"+i[e%i.length])}const n={};let r=0;return t>0&&(r=t),e&&Object.keys(e).forEach(t=>{const i=e[t];isFinite(i)?n[t.toLowerCase()]=a(i):n[t.toLowerCase()]=Color(e[t])}),function(e,t){let i;const s=t[3];if(null===s)return Color().hsl(0,40,38);if(void 0===s)return Color().hsl(120,40,38);const o=s.toLowerCase();return void 0===i&&(i=n[o]),void 0===i&&(i=a(r),r++,n[o]=i),i}}}customElements.define("ha-chart-base",p);class f extends(Object(r.a)(n.a)){static get template(){return a.a`
      <style>
        :host {
          display: block;
          overflow: hidden;
          height: 0;
          transition: height 0.3s ease-in-out;
        }
      </style>
      <ha-chart-base
        id="chart"
        data="[[chartData]]"
        identifier="[[identifier]]"
        rendered="{{rendered}}"
      ></ha-chart-base>
    `}static get properties(){return{chartData:Object,data:Object,names:Object,unit:String,identifier:String,isSingleDevice:{type:Boolean,value:!1},endTime:Object,rendered:{type:Boolean,value:!1,observer:"_onRenderedChanged"}}}static get observers(){return["dataChanged(data, endTime, isSingleDevice)"]}connectedCallback(){super.connectedCallback(),this._isAttached=!0,this.drawChart()}dataChanged(){this.drawChart()}_onRenderedChanged(e){e&&this.animateHeight()}animateHeight(){requestAnimationFrame(()=>requestAnimationFrame(()=>{this.style.height=this.$.chart.scrollHeight+"px"}))}drawChart(){const e=this.unit,t=this.data,i=[];let a;if(!this._isAttached)return;if(0===t.length)return;function n(e){const t=parseFloat(e);return isFinite(t)?t:null}a=this.endTime||new Date(Math.max.apply(null,t.map(e=>new Date(e.states[e.states.length-1].last_changed)))),a>new Date&&(a=new Date);const r=this.names||{};t.forEach(t=>{const s=t.domain,o=r[t.entity_id]||t.name;let c;const l=[];function d(e,t){t&&(e>a||(l.forEach((i,a)=>{i.data.push({x:e,y:t[a]})}),c=t))}function h(t,i,a){let n=!1,r=!1;a&&(n="origin"),i&&(r="before"),l.push({label:t,fill:n,steppedLine:r,pointRadius:0,data:[],unitText:e})}if("thermostat"===s||"climate"===s||"water_heater"===s){const e=t.states.some(e=>e.attributes&&e.attributes.hvac_action),i="climate"===s&&e?e=>"heating"===e.attributes.hvac_action:e=>"heat"===e.state,a="climate"===s&&e?e=>"cooling"===e.attributes.hvac_action:e=>"cool"===e.state,r=t.states.some(i),c=t.states.some(a),l=t.states.some(e=>e.attributes&&e.attributes.target_temp_high!==e.attributes.target_temp_low);h(""+this.hass.localize("ui.card.climate.current_temperature","name",o),!0),r&&h(""+this.hass.localize("ui.card.climate.heating","name",o),!0,!0),c&&h(""+this.hass.localize("ui.card.climate.cooling","name",o),!0,!0),l?(h(""+this.hass.localize("ui.card.climate.target_temperature_mode","name",o,"mode",this.hass.localize("ui.card.climate.high")),!0),h(""+this.hass.localize("ui.card.climate.target_temperature_mode","name",o,"mode",this.hass.localize("ui.card.climate.low")),!0)):h(""+this.hass.localize("ui.card.climate.target_temperature_entity","name",o),!0),t.states.forEach(e=>{if(!e.attributes)return;const t=n(e.attributes.current_temperature),s=[t];if(r&&s.push(i(e)?t:null),c&&s.push(a(e)?t:null),l){const t=n(e.attributes.target_temp_high),i=n(e.attributes.target_temp_low);s.push(t,i),d(new Date(e.last_changed),s)}else{const t=n(e.attributes.temperature);s.push(t),d(new Date(e.last_changed),s)}})}else if("humidifier"===s)h(""+this.hass.localize("ui.card.humidifier.target_humidity_entity","name",o),!0),h(""+this.hass.localize("ui.card.humidifier.on_entity","name",o),!0,!0),t.states.forEach(e=>{if(!e.attributes)return;const t=n(e.attributes.humidity),i=[t];i.push("on"===e.state?t:null),d(new Date(e.last_changed),i)});else{h(o,"sensor"===s);let e=null,i=null,a=null;t.states.forEach(t=>{const r=n(t.state),s=new Date(t.last_changed);if(null!==r&&null!==a){const t=s.getTime(),n=a.getTime(),o=i.getTime();d(a,[(n-o)/(t-o)*(r-e)+e]),d(new Date(n+1),[null]),d(s,[r]),i=s,e=r,a=null}else null!==r&&null===a?(d(s,[r]),i=s,e=r):null===r&&null===a&&null!==e&&(a=s)})}d(a,c),Array.prototype.push.apply(i,l)});const s={type:"line",unit:e,legend:!this.isSingleDevice,options:{scales:{xAxes:[{type:"time",ticks:{major:{fontStyle:"bold"}}}],yAxes:[{ticks:{maxTicksLimit:7}}]},tooltips:{mode:"neareach",callbacks:{title:(e,t)=>{const i=e[0],a=t.datasets[i.datasetIndex].data[i.index].x;return Object(o.b)(a,this.hass.language)}}},hover:{mode:"neareach"},layout:{padding:{top:5}},elements:{line:{tension:.1,pointRadius:0,borderWidth:1.5},point:{hitRadius:5}},plugins:{filler:{propagate:!0}}},data:{labels:[],datasets:i}};this.chartData=s}}customElements.define("state-history-chart-line",f);var m=i(120);class g extends(Object(r.a)(n.a)){static get template(){return a.a`
      <style>
        :host {
          display: block;
          opacity: 0;
          transition: opacity 0.3s ease-in-out;
        }
        :host([rendered]) {
          opacity: 1;
        }

        ha-chart-base {
          direction: ltr;
        }
      </style>
      <ha-chart-base
        data="[[chartData]]"
        rendered="{{rendered}}"
        rtl="{{rtl}}"
      ></ha-chart-base>
    `}static get properties(){return{hass:{type:Object},chartData:Object,data:{type:Object,observer:"dataChanged"},names:Object,noSingle:Boolean,endTime:Date,rendered:{type:Boolean,value:!1,reflectToAttribute:!0},rtl:{reflectToAttribute:!0,computed:"_computeRTL(hass)"}}}static get observers(){return["dataChanged(data, endTime, localize, language)"]}connectedCallback(){super.connectedCallback(),this._isAttached=!0,this.drawChart()}dataChanged(){this.drawChart()}drawChart(){let e=this.data;if(!this._isAttached)return;e||(e=[]);const t=new Date(e.reduce((e,t)=>Math.min(e,new Date(t.data[0].last_changed)),new Date));let i=this.endTime||new Date(e.reduce((e,t)=>Math.max(e,new Date(t.data[t.data.length-1].last_changed)),t));i>new Date&&(i=new Date);const a=[],n=[],r=this.names||{};e.forEach(e=>{let s,o=null,c=null,l=t;const d=r[e.entity_id]||e.name,h=[];e.data.forEach(e=>{let t=e.state;void 0!==t&&""!==t||(t=null),new Date(e.last_changed)>i||(null!==o&&t!==o?(s=new Date(e.last_changed),h.push([l,s,c,o]),o=t,c=e.state_localize,l=s):null===o&&(o=t,c=e.state_localize,l=new Date(e.last_changed)))}),null!==o&&h.push([l,i,c,o]),n.push({data:h}),a.push(d)});const s={type:"timeline",options:{tooltips:{callbacks:{label:(e,t)=>{const i=t.datasets[e.datasetIndex].data[e.index],a=Object(o.b)(i[0],this.hass.language),n=Object(o.b)(i[1],this.hass.language);return[i[2],a,n]}}},scales:{xAxes:[{ticks:{major:{fontStyle:"bold"}}}],yAxes:[{afterSetDimensions:e=>{e.maxWidth=.18*e.chart.width},position:this._computeRTL?"right":"left"}]}},data:{labels:a,datasets:n},colors:{staticColors:{on:1,off:0,unavailable:"#a0a0a0",unknown:"#606060",idle:2},staticColorIndex:3}};this.chartData=s}_computeRTL(e){return Object(m.a)(e)}}customElements.define("state-history-chart-timeline",g);class b extends(Object(r.a)(n.a)){static get template(){return a.a`
      <style>
        :host {
          display: block;
          /* height of single timeline chart = 58px */
          min-height: 58px;
        }
        .info {
          text-align: center;
          line-height: 58px;
          color: var(--secondary-text-color);
        }
      </style>
      <template
        is="dom-if"
        class="info"
        if="[[_computeIsLoading(isLoadingData)]]"
      >
        <div class="info">
          [[localize('ui.components.history_charts.loading_history')]]
        </div>
      </template>

      <template
        is="dom-if"
        class="info"
        if="[[_computeIsEmpty(isLoadingData, historyData)]]"
      >
        <div class="info">
          [[localize('ui.components.history_charts.no_history_found')]]
        </div>
      </template>

      <template is="dom-if" if="[[historyData.timeline.length]]">
        <state-history-chart-timeline
          hass="[[hass]]"
          data="[[historyData.timeline]]"
          end-time="[[_computeEndTime(endTime, upToNow, historyData)]]"
          no-single="[[noSingle]]"
          names="[[names]]"
        ></state-history-chart-timeline>
      </template>

      <template is="dom-repeat" items="[[historyData.line]]">
        <state-history-chart-line
          hass="[[hass]]"
          unit="[[item.unit]]"
          data="[[item.data]]"
          identifier="[[item.identifier]]"
          is-single-device="[[_computeIsSingleLineChart(item.data, noSingle)]]"
          end-time="[[_computeEndTime(endTime, upToNow, historyData)]]"
          names="[[names]]"
        ></state-history-chart-line>
      </template>
    `}static get properties(){return{hass:Object,historyData:{type:Object,value:null},names:Object,isLoadingData:Boolean,endTime:{type:Object},upToNow:Boolean,noSingle:Boolean}}_computeIsSingleLineChart(e,t){return!t&&e&&1===e.length}_computeIsEmpty(e,t){const i=!t||!t.timeline||!t.line||0===t.timeline.length&&0===t.line.length;return!e&&i}_computeIsLoading(e){return e&&!this.historyData}_computeEndTime(e,t){return t?new Date:e}}customElements.define("state-history-charts",b)},612:function(e,t,i){"use strict";i.r(t);i(262),i(190);var a=i(4),n=i(32),r=(i(191),i(131),i(347),i(174)),s=i(12),o=(i(346),i(287));class c extends n.a{static get template(){return a.a`
      <style include="iron-flex ha-style">
        .content {
          padding-bottom: 32px;
        }
        .border {
          margin: 32px auto 0;
          border-bottom: 1px solid rgba(0, 0, 0, 0.12);
          max-width: 1040px;
        }
        .narrow .border {
          max-width: 640px;
        }
        div.aisInfoRow {
          display: inline-block;
        }
        .center-container {
          @apply --layout-vertical;
          @apply --layout-center-center;
          height: 70px;
        }
        ha-icon-button {
          vertical-align: middle;
        }
      </style>

      <hass-subpage header="Konfiguracja bramki AIS dom">
        <div class$="[[computeClasses(isWide)]]">
          <ha-config-section is-wide="[[isWide]]">
            <span slot="header">Połączenie WiFi</span>
            <span slot="introduction"
              >Możesz sprawdzić lub skonfigurować parametry połączenia
              WiFi</span
            >
            <ha-card header="Parametry sieci">
              <div class="card-content" style="display: flex;">
                <div style="text-align: center;">
                  <div class="aisInfoRow">Lokalna nazwa hosta</div>
                  <div class="aisInfoRow">
                    <mwc-button on-click="showLocalIpInfo"
                      >[[aisLocalHostName]]</mwc-button
                    ><ha-icon-button
                      class="user-button"
                      icon="hass:settings"
                      on-click="createFlowHostName"
                    ></ha-icon-button>
                  </div>
                </div>
                <div on-click="showLocalIpInfo" style="text-align: center;">
                  <div class="aisInfoRow">Lokalny adres IP</div>
                  <div class="aisInfoRow">
                    <mwc-button>[[aisLocalIP]]</mwc-button>
                  </div>
                </div>
                <div on-click="showWiFiSpeedInfo" style="text-align: center;">
                  <div class="aisInfoRow">Prędkość połączenia WiFi</div>
                  <div class="aisInfoRow">
                    <mwc-button>[[aisWiFiSpeed]]</mwc-button>
                  </div>
                </div>
              </div>
              <div class="card-actions">
                <div>
                  <ha-icon-button
                    class="user-button"
                    icon="hass:wifi"
                    on-click="showWiFiGroup"
                  ></ha-icon-button
                  ><mwc-button on-click="createFlowWifi"
                    >Konfigurator połączenia z siecą WiFi</mwc-button
                  >
                </div>
              </div>
            </ha-card>
          </ha-config-section>
        </div>
      </hass-subpage>
    `}static get properties(){return{hass:Object,isWide:Boolean,showAdvanced:Boolean,aisLocalHostName:{type:String,computed:"_computeAisLocalHostName(hass)"},aisLocalIP:{type:String,computed:"_computeAisLocalIP(hass)"},aisWiFiSpeed:{type:String,computed:"_computeAisWiFiSpeed(hass)"},_config:Object,_names:Object,_entities:Array,_cacheConfig:Object}}computeClasses(e){return e?"content":"content narrow"}_computeAisLocalHostName(e){return e.states["sensor.local_host_name"].state}_computeAisLocalIP(e){return e.states["sensor.internal_ip_address"].state}_computeAisWiFiSpeed(e){return e.states["sensor.ais_wifi_service_current_network_info"].state}showWiFiGroup(){Object(s.a)(this,"hass-more-info",{entityId:"group.internet_status"})}showWiFiSpeedInfo(){Object(s.a)(this,"hass-more-info",{entityId:"sensor.ais_wifi_service_current_network_info"})}showLocalIpInfo(){Object(s.a)(this,"hass-more-info",{entityId:"sensor.internal_ip_address"})}_continueFlow(e){Object(r.b)(this,{continueFlowId:e,dialogClosedCallback:()=>{console.log("OK")}})}createFlowHostName(){this.hass.callApi("POST","config/config_entries/flow",{handler:"ais_host"}).then(e=>{this._continueFlow(e.flow_id)})}createFlowWifi(){this.hass.callApi("POST","config/config_entries/flow",{handler:"ais_wifi_service"}).then(e=>{console.log(e),this._continueFlow(e.flow_id)})}ready(){super.ready();const e=Object(o.a)(["sensor.ais_wifi_service_current_network_info"]),t=[],i={};for(const a of e)t.push(a.entity),a.name&&(i[a.entity]=a.name);this.setProperties({_cacheConfig:{cacheKey:t.join(),hoursToShow:24,refresh:0},_entities:t,_names:i})}}customElements.define("ha-config-ais-dom-config-wifi",c)}}]);
//# sourceMappingURL=chunk.968d93520833db613d56.js.map