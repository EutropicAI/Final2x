<script lang="ts" setup>
import { FilmOutline } from '@vicons/ionicons5'

class openWebsite {
  static async FinalRip(): Promise<void> {
    window.open('https://github.com/EutropicAI/FinalRip', '_blank')
  }

  static async VSET(): Promise<void> {
    window.open('https://github.com/EutropicAI/VSET', '_blank')
  }
}
</script>

<template>
  <div class="MyExternalLink">
    <n-space>
      <n-button style="font-size: 36px" text @click="openWebsite.VSET">
        <n-icon>
          <FilmOutline />
        </n-icon>
      </n-button>
    </n-space>
  </div>
</template>

<style lang="scss" scoped>
.custom-fade-enter-active {
  transition: all 2s ease-out;
}

.custom-fade-leave-active {
  transition: all 2s cubic-bezier(1, 0.5, 0.8, 1);
}

.custom-fade-enter-from,
.custom-fade-leave-to {
  opacity: 0;
}
</style>
