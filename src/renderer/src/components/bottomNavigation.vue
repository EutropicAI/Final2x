<script lang="ts" setup>
import MyExternalLink from './MyExternalLink.vue'
import MySetting from './MySetting.vue'
</script>

<template>
  <div class="position">
    <n-divider class="n-divider" />
    <n-space class="n-space" justify="space-between">
      <MySetting />
      <MyExternalLink />
    </n-space>
  </div>
</template>

<style lang="scss" scoped>
.position {
  box-sizing: border-box;
  width: 100%;
  height: 60px;
  justify-content: flex-end;
}

.n-space {
  box-sizing: border-box;
  margin: 10px 20px 0 20px;
}

.n-divider {
  margin: 0 !important;
}
</style>
