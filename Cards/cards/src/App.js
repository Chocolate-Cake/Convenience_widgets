import React from 'react';
import './App.css';
import * as XLSX from 'xlsx';

class App extends React.Component {

  state = {
    defs: {},
    uploader_style: {
      float: 'left', 
      width: window.innerWidth * 0.25, 
      height: window.innerHeight * 0.1,
      border: 'solid black 1px'
    },
    scorer_style: {
      float: 'left', 
      width: window.innerWidth * 0.7, 
      height: window.innerHeight * 0.1,
      border: 'solid black 1px'
    },
    cards_box_style: {
      float: 'left', 
      width: window.innerWidth * 0.75, 
      height: window.innerHeight * 0.8,
      border: 'solid black 1px'
    },
    categories_style: {
      float: 'left', 
      width: window.innerWidth * 0.2, 
      height: window.innerHeight * 0.8,
      border: 'solid black 1px'
    }
  }

  handleUpload(e) {
    e.preventDefault();
    var f = this.refs.file_select.files[0];
    var reader = new FileReader();
    reader.onload = function(e) {
      var data = new Uint8Array(e.target.result);
      var workbook = XLSX.read(data, {type: 'array'});
      var j = XLSX.utils.sheet_to_json(workbook['Sheets']['Sheet1']);
      console.log(j);
    };
    reader.readAsArrayBuffer(f);

    //TODO clean data and put in state
  }

  handleSave(e) {
    //TODO
  }


  /*
  Features TODO
  - allow management of categories
  - allow selection/ignoring of categories
  - create cards that flip and unflip
  - allow pressing keys to interact instead of requiring clicks
  - allow gamification
  - error checking
  */

  render() { 
      return (
      <div className="App" style={{margin: window.innerWidth * 0.02}}>

      <div>
      <div ref="uploader" style={this.state.uploader_style}>
        <input ref='file_select' type='file'/>
        <input type='submit' value='Upload' onClick={(e) => this.handleUpload(e)}/>
        <div style={{width: '100%', border: '1px dotted black'}}/>
        File name: <input ref='save_name' type='text'/>
        <input type='submit' value='Save'/>
      </div>

      <div ref="scorer" style={this.state.scorer_style}>
        placeholder text 
      </div>
      </div>
      <div>
      <div ref="cards_box" style={this.state.cards_box_style}>
        placeholder text
      </div>

      <div ref="categories" style={this.state.categories_style}>
        placeholder text
      </div>
      </div>
      </div>
    );
  }
}

export default App;
