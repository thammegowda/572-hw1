# Interactive Selenium Plugin
  Nutch comes with preconfigured interactive selenium plugin, located at `src/plugin/protocol-interactiveselenium`.
  It uses firefox web driver by default when enabled.

## Enable plugin
1. Goto conf/nutch-site.xml

   (If not already present, copy the property config `plugin.includes` from nutch-default.xml to nutch-site.xml)  
   Replace `protocol-http` plugin with `protocol-interactiveselenium`.  
   It should look like :  
    ```xml
<property>
  <name>plugin.includes</name>
  <value>protocol-interactiveselenium|urlfilter-regex| ... </value>
  <description></description>
</property>
```
2. Add custom handler.

To create a custom handler, refer the `org.apache.nutch.protocol.interactiveselenium.handlers.DefaultHandler` example in the supplied plugin. After creating the handler, it needs to be registered in config. In the same config file as previous step, add the following config:

```xml
<property>
  <name>interactiveselenium.handlers</name>
   <value>handlers.NewCustomHandler,DefaultHandler</value>
   <description></description>
</property>
```

Make sure to place NewCustomHandler class in `org.apache.nutch.protocol.interactiveselenium.handlers` package when you register as `handlers.NewCustomHandler`.

---


       
