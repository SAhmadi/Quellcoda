<template>
  <div class="tree">
    <div class="tree-header">
      FILES
    </div>

    <ul class="tree-list">
      <node-tree :node="tree"></node-tree>
    </ul>

    <div class="action-btn" @click="addNewFile" style="width:100px;">
      <span>+ NEW FILE</span>
    </div>

    <div class="action-btn" @click="addNewDirectory">
      <span>+ NEW DIRECTORY</span>
    </div>
  </div>
</template>

<script>
import NodeTree from "./NodeTree";

export default {
  name: 'file-tree',
  props: {
    treeData: Object,
    models: Array,
  },
  components: {
    NodeTree
  },
  data: function() {
    return {
    };
  },
  computed: {
    tree() {
      return {
        children: this.$store.getters.fileTreeChildren,
      };
    },
  },
  methods: {
    addNewFile() {
      // Determine path of new file
      let currActiveNode = this.$store.getters.activeNode;
      let newFilePath = ''; // set to root folder
      if (currActiveNode.children) {
        // if active node is directory get its path
        newFilePath = `${currActiveNode.path}/${currActiveNode.name}/`;
      }

      let fileCounter = this.$store.getters.newFileCounter;
      let file = {
        id: fileCounter,
        path: newFilePath,
        name: 'NewFile' + fileCounter + '.java',
        model: {
          value: '// Enter your code here...',
          language: 'java'
        },
      };
      this.$store.dispatch('updateNewFileCounter', fileCounter + 1);

      // Create Model
      let model = {
        id: file.id,
        path: file.path,
        name: file.name,
        value: file.model.value,
        language: file.model.language,
      };

      this.$store.dispatch('updateModels', model);

      if (currActiveNode.children) {
        // If active node is directory add new file to it
        currActiveNode.children.push(file);
      }
      else {
        // Otherwise add new file to root folder
        let newTreeData = this.$store.getters.fileTreeChildren;
        newTreeData.push(file);
        this.$store.dispatch('updateFileTree', newTreeData);
      }
    },

    addNewDirectory() {
      // Determine path of new file
      let currActiveNode = this.$store.getters.activeNode;
      let newDirPath = ''; // set to root folder
      if (currActiveNode.children) {
        // if active node is directory get its path
        newDirPath = `${currActiveNode.path}/${currActiveNode.name}/`;
      }

      let fileCounter = this.$store.getters.newFileCounter;
      let dir = {
        id: fileCounter,
        path: newDirPath,
        name: 'new_dir_' + fileCounter,
        children: [],
      };
      this.$store.dispatch('updateNewFileCounter', fileCounter + 1);

      if (currActiveNode.children) {
        currActiveNode.children.push(dir);
      }
      else {
        let newTreeData = this.$store.getters.fileTreeChildren;
        newTreeData.push(dir);
        this.$store.dispatch('updateFileTree', newTreeData);
      }
    },
  },
};
</script>

<style lang="scss">
.tree {
  /*width: 300px;*/
  height: 100%;
  position: absolute;
  background: #f0f0f5;
}

.tree-header {
  width: 100%;
  height: 30px;
  background: #e0e0e5;
  font-weight: bold;
  padding-top: 3px;
  padding-left: 16px;
  border-bottom: solid 1px #ccc;
}

.tree-list {
  padding: 0;
}

.action-btn {
  width: 150px;
  font-size: 14px;
  font-weight: bold;
  background: #ddd;
  margin-left: 20px;
  margin-bottom: 10px;
  border-radius: 2px;

  span {
    line-height: 190%;
    padding-left: 9px;
  }
}
.action-btn:hover {
  background: #ccc;
  cursor: pointer;
}
</style>