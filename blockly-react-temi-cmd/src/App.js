import React, { useRef, useState } from "react";
import BlocklyComponent, { Block, Value, Field, Category } from "./Blockly";
import BlocklyPython from "blockly/python";
import { babyAiService, babyAiServiceTemi, exportWorkspace, downloadSavedWorkspace } from "./services/babyAiService";
import { CodeBlock, dracula } from "react-code-blocks";
import Blockly from 'blockly'

import "./blocks/customblocks";
import "./generator/generator";
import "./App.css";

//Container of result from server
const ConsoleComponent = ({ data = [] }) => {
  const items = data.map((val, index) => {
    return (
      <div className="itemsResult" key={index}>
        {val}
      </div>
    );
  });
  return (
    <>
      <p style={{ padding: "0 5px" }}>
        <b>Output Result</b>
      </p>
      <div className="wrapperItemResult">{items}</div>
    </>
  );
};

//Top bar componenet NOTE that save and load is in developed
const NavbarComponent = ({ generateCode, toggle, save, input}) => {
  return (
    <div
      style={{
        display: "flex",
        flexDirection: "row",
        alignItems: "center",
        padding: "10px",
        borderBottom: "1px solid #d2d2d2",
      }}
    >
      <div style={{ flex: 1 }}>
        <h3
          style={{
            padding: 0,
            margin: 0,
          }}
        >
          TEMI Block Programming
        </h3>
      </div>
      <div style={{}}>
        <button onClick={toggle} className="previewBtn">
          Preview
        </button>
        <button onClick={generateCode} className="compileBtn">
          Execute
        </button>
        {/* Wait for API Line to save and download xml file */}
        <button onClick={save} className="saveBtn">
          Save
        </button>
        <input type="file" name="file" onChange={input} className="custom-file-input"/>
        
      </div>
    </div>
  );
};

//Blockly workspace html, you may add your defined block here
const WorkspaceComponent = ({ initWorkspaceRef }) => {
  return (
    <BlocklyComponent
      ref={(instanceRef) => {
        initWorkspaceRef(instanceRef);
      }}
      readOnly={false}
      trashcan={true}
      media={"media/"}
      move={{ scrollbars: true, drag: true, wheel: true }}
    >
      <Category name="Logic" colour="210">
        <Block type="controls_if"></Block>
        <Block type="logic_compare"></Block>
        <Block type="logic_operation"></Block>
        <Block type="logic_negate"></Block>
        <Block type="logic_boolean"></Block>
      </Category>
      <Category name="Loops" colour="120">
        <Block type="controls_repeat_ext">
          <Value name="TIMES">
            <Block type="math_number">
              <Field name="NUM">10</Field>
            </Block>
          </Value>
        </Block>
        <Block type="controls_whileUntil"></Block>
      </Category>
      <Category name="Text" colour="20">
        <Block type="text"></Block>
        <Block type="text_length"></Block>
        <Block type="text_print"></Block>
      </Category>
      <Category name="Math" colour="230">
        <Block type="math_number"></Block>
        <Block type="math_arithmetic"></Block>
        <Block type="math_single"></Block>
      </Category>

      <Category name="Temi Skill" colour="300">
        <Block type="temi_start"></Block>
        <Block type="speech_say"></Block>
        <Block type="locations_goto"></Block>
        <Block type="follow_constrained"></Block>
        <Block type="movement_turn"></Block>
        <Block type="locations_go_home"></Block>
        <Block type="call_person"></Block>
        <Block type="movement"></Block>
        <Block type="movement_tilt"></Block>
        <Block type="movement_joystick"></Block>
        <Block type="follow_unconstrained"></Block>
      </Category>

      <Category name="Event" colour="300">
        <Block type="event_block"></Block>
      </Category>
      
    </BlocklyComponent>
  );
};

//Main application window
const App = () => {
  var loadedContent = ""
  var savedFilename = ""
  const workspaceRef = useRef(null); //workspace ref

  const [togglePreviewCode, setTogglePreviewCode] = useState(false);
  const [executeCodeResponse, setExecuteCodeResponse] = useState([]);
  const [codePreview, setCodePreview] = useState("");

  const getCode = () => {
    let codeFromBlock = BlocklyPython.workspaceToCode(
      workspaceRef.current.workspace
    );

    setCodePreview(codeFromBlock);
    return codeFromBlock;
  };

  const saveWorkspace = () => {
    try {
      var xml = Blockly.Xml.workspaceToDom(workspaceRef.current.workspace); //convert all block to xml
      var xml_text = Blockly.Xml.domToText(xml); //convert xml to text
      const response =  exportWorkspace(xml_text).then( res => {
        //Open an new browser tab to trigger built-in downloader 
        savedFilename = res.data.split(',')[1].split(':')[1];
        const BASE_URL = `http://babyai.org:5000/workspace/export/download/` + savedFilename.replace(/'/g, '');
        const HEADERS = {
          "Accept" : "*/*",
        };
        window.open(BASE_URL, '_blank')
      }).catch(err => {
        alert(err);
      });

      }catch(e) {
        alert(e)
      }
  }
  const loadWorkspace = () => {
    try {
      const XML = Blockly.Xml.textToDom(loadedContent)
      Blockly.Xml.clearWorkspaceAndLoadFromXml(XML, workspaceRef.current.workspace)
    }catch(e){
      alert(e)
      alert('File may be corrupted!')
    }

  }

  //Generate code from block connection
  const generateCode = async () => {
    const codeFromBlock = getCode();
    console.log(codeFromBlock)
    try{
      console.log(codeFromBlock);
      // const response = await babyAiServiceTemi(code);
      const response = await babyAiService(codeFromBlock)
    // const response = await babyAiService(code);
    //Set output console to try exexting
    // ConsoleComponent(["Try Executing",]);
    setExecuteCodeResponse(response.data.split("\n"));
    }catch(e) {
      alert('Cannot execute a code for reason: ' + e)
    }
  };
  //Toggle preview code besied OUTPUT tab
  const onHandlerTogglePreviewCode = () => {
    const toggle = togglePreviewCode ? false : true;
    getCode();
    setTogglePreviewCode(toggle);
  };

  const onFileChangeHandle = (event) => {
    try {
      const reader = new FileReader();
      reader.onload = (e) => {
        const text = (e.target.result)
        loadedContent = text;
        loadWorkspace();
      }
      reader.readAsText(event.target.files[0])
    }catch(e) {
      console.log(e)
    }
  }
  //TEST
  function rtCodeUpdateFunction(event) {
    var code = getCode();
    setCodePreview(code);
  }
  //Main rendered window, blockly workspace reference object is called here
  return (
    <>
      <NavbarComponent
        generateCode={generateCode}
        toggle={onHandlerTogglePreviewCode}
        save={saveWorkspace}
        input={onFileChangeHandle}
      />
        <WorkspaceComponent
          initWorkspaceRef={(ref) => {
            workspaceRef.current = ref;
            // Prevent flyout from automatically closed
            Blockly.Flyout.prototype.autoClose = false;
            // Blockly.Workspace.addChangeListener(getCode)
           // workspaceRef.current.addChangeListener(getCode)
            //Add real-time code generation callback
            
          }}/>
      <div>
      {/* PREVIEW button is press (toggle state), disply output*/}
      <div style={{ display: togglePreviewCode ? "none" : "initial" }}> 
        <ConsoleComponent data={executeCodeResponse.map((val) => `> ${val}`)} />
      </div>
 
      {/* PREVIEW button is press (toggle state), display python code and output side by side*/}
      <div style={{ display: togglePreviewCode ? "initial" : "none" }}> 
          <div className="wrapperToggleView">
            <div className="box">
              <ConsoleComponent data={executeCodeResponse.map((val) => `> ${val}`)} />
            </div>

            <div className="box">    
            <p style={{ padding: "0 5px" }}>
              <b>Python Code</b>
            </p>      
              <CodeBlock
                 text={
                    codePreview === ""
                      ? "🔥 #Let's Started 🔥 \n\n\n\n\n\n\n\n\n"
                      : codePreview
                  }
                  language={"python"}
                  showLineNumbers={true}
                  theme={dracula}
                  codeBlock
              />
            </div>
          </div>
      </div>
      
      </div>
      
    </>
  );
};

export default App;