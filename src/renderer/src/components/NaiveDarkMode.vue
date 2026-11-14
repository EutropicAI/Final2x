<script lang="ts" setup>
import type { PropType, Ref } from 'vue'
import { darkTheme, useOsTheme } from 'naive-ui'
import { nextTick, onBeforeMount, onMounted, ref, watch } from 'vue'

export type NaiveDarkModeType = undefined | 'light' | 'dark' | 'system'

// 不想用 CSS Transition，可以用 JS 实现捏

// -----------------------------------------------------------------------------
// Props and Emits
// -----------------------------------------------------------------------------

const props = defineProps({
  darkMode: {
    type: String as PropType<NaiveDarkModeType>,
    default: () => 'system',
  },
  designDark: {
    type: String,
    default: () => '#000000',
  },
  designLight: {
    type: String,
    default: () => '#ffffff',
  },
  fadeLayer: {
    type: Number,
    default: () => 25,
  },
  color: {
    type: String,
    default: () => '#ffffff',
  },
  naivetheme: {
    type: Object,
    default: () => undefined,
  },
})

const emits = defineEmits(['update:color', 'update:naivetheme'])

// -----------------------------------------------------------------------------
// Refs
// -----------------------------------------------------------------------------

const osThemeRef = useOsTheme()

const DarkMode: Ref<NaiveDarkModeType> = ref(undefined)
const globalcolor = ref('')
const DarkTheme: Ref<boolean | undefined> = ref(undefined)
const DesignDarkColor = ref('#000000')
const DesignLightColor = ref('#ffffff')
const FadeLayer = ref(25)

// v-model 传入的 color
watch(
  () => globalcolor.value,
  (value) => {
    emits('update:color', value)
  },
)

// v-model 传入的 naivetheme
watch(
  () => DarkTheme.value,
  (value) => {
    emits('update:naivetheme', value ? darkTheme : undefined)
  },
)

onBeforeMount(() => {
  // 传入
  DarkMode.value = props.darkMode
  DesignDarkColor.value = props.designDark
  DesignLightColor.value = props.designLight
  // set designLightColor to globalcolor, update:color
  globalcolor.value = props.designLight
  FadeLayer.value = props.fadeLayer
  // console.log('onBeforeMount  DarkMode.value', DarkMode.value)
})

// 监听 props.darkMode 的变化
watch(
  () => props.darkMode,
  (value) => {
    DarkMode.value = value
  },
)

// 监听 props.designDark 的变化
watch(
  () => props.designDark,
  (value) => {
    if (globalcolor.value === DesignDarkColor.value) {
      globalcolor.value = value
    }
    DesignDarkColor.value = value
  },
)

// 监听 props.designLight 的变化
watch(
  () => props.designLight,
  (value) => {
    if (globalcolor.value === DesignLightColor.value) {
      globalcolor.value = value
    }
    DesignLightColor.value = value
  },
)

// 监听 props.fadeLayer 的变化
watch(
  () => props.fadeLayer,
  (value) => {
    FadeLayer.value = value
  },
)

/**
 * @description update DarkTheme.value and update:naivetheme
 * @param mode 'dark' or 'light' or 'system'
 */
function handleDarkModeChange(mode: NaiveDarkModeType): void {
  // console.log('handleDarkModeChange  DarkTheme.value', DarkTheme.value)
  // console.log('handleDarkModeChange  mode', mode)
  if (mode === 'system' || mode === undefined) {
    DarkTheme.value = osThemeRef.value === 'dark'
  }
  else {
    DarkTheme.value = mode === 'dark'
  }
}

onMounted(() => {
  // console.log('onMounted  DarkMode.value', DarkMode.value)
  handleDarkModeChange(DarkMode.value)
})

watch(DarkMode, (value) => {
  // console.log('watch DarkMode  ', value)
  handleDarkModeChange(value)
})

// 检测系统主题，修改 DarkTheme.value
watch(osThemeRef, (value) => {
  // console.log('watch  osThemeRef', value)
  if (DarkMode.value === 'system' || DarkMode.value === undefined) {
    DarkTheme.value = value === 'dark'
  }
})

// 检测 DarkTheme.value，修改 CSS 样式
watch(DarkTheme, (value) => {
  // console.log('watch DarkTheme  ', value)
  if (value) {
    if (isCSSLight()) {
      switchCSSStyle('dark')
    }
  }
  else {
    if (isCSSDark()) {
      switchCSSStyle('light')
    }
  }
})

// -----------------------------------------------------------------------------
// Functions
// -----------------------------------------------------------------------------

/**
 * @description Interpolate two colors by a given factor
 */
function interpolateColor(color1: string, color2: string, factor: number): string {
  if (factor === 0)
    return color1
  if (factor === 1)
    return color2

  const c1 = hexToRgb(color1)
  const c2 = hexToRgb(color2)

  const r = Math.round(interpolate(c1.r, c2.r, factor))
  const g = Math.round(interpolate(c1.g, c2.g, factor))
  const b = Math.round(interpolate(c1.b, c2.b, factor))

  return `rgb(${r}, ${g}, ${b})`
}

function interpolate(start: number, end: number, factor: number): number {
  return start + (end - start) * factor
}

function hexToRgb(hex: string): { r: number, g: number, b: number } {
  const r = Number.parseInt(hex.slice(1, 3), 16)
  const g = Number.parseInt(hex.slice(3, 5), 16)
  const b = Number.parseInt(hex.slice(5, 7), 16)
  return { r, g, b }
}

/**
 * @description Smooth transition to dark mode
 * @param mode 'dark' or 'light' or 'system'
 */
function switchCSSStyle(mode: NaiveDarkModeType): void {
  if (mode === 'system') {
    const osThemeRef = useOsTheme()
    mode = osThemeRef.value === 'dark'
      ? 'dark'
      : 'light'
  }
  const targetColor = mode === 'dark'
    ? DesignDarkColor.value
    : DesignLightColor.value
  const initialColor = mode === 'dark'
    ? DesignLightColor.value
    : DesignDarkColor.value
  const layer = Math.ceil(FadeLayer.value)

  if (layer < 1) {
    globalcolor.value = targetColor
    return
  }

  for (let i = 1; i <= layer; i++) {
    setTimeout(() => {
      nextTick(() => {
        globalcolor.value = interpolateColor(initialColor, targetColor, i / layer)
      })
    }, layer * i)
  }
}

/**
 * @description Check if the current CSS theme is dark
 */
function isCSSDark(): boolean {
  return globalcolor.value === DesignDarkColor.value
}

/**
 * @description Check if the current CSS theme is light
 */
function isCSSLight(): boolean {
  return globalcolor.value === DesignLightColor.value
}
</script>

<template>
  <div />
</template>

<style lang="scss"></style>
