import { LANG_LIST } from '../plugins/i18n'

class Utils {
  /**
   * @description 返回语言，和语言数量
   * @param id language id: 0-> en, 1-> zh, 2-> ja, 3-> fr, 4-> tr
   */
  static getLanguage(id: number): { lang: string, numLang: number } {
    const langs = LANG_LIST
    return {
      lang: langs[id],
      numLang: langs.length,
    }
  }

  /**
   * @description 等待一段时间
   * @param timeout 等待时间，单位毫秒
   */
  static sleep(timeout: number): Promise<void> {
    return new Promise(resolve => setTimeout(resolve, timeout))
  }

  /**
   * @description Deep, Dark, Fantasy? 真·深度睡眠
   * @param miliseconds 等待时间，单位毫秒
   */
  static DeepDeepSleep(miliseconds: number): void {
    const currentTime = new Date().getTime()
    while (currentTime + miliseconds >= new Date().getTime()) {
      /* empty */
    }
  }

  /**
   * @description 生成超长随机字符串
   */
  static getRandString(): string {
    return Math.random().toString(36).substring(2, 15) + Math.random().toString(36).substring(2, 15)
  }

  /**
   * @description: 防抖函数装饰器，防止用户频繁点击
   * @param fn  需要防抖的函数
   * @param delay 防抖的时间间隔，默认500ms
   */
  static clickDebounce(
    fn: (...args: any[]) => void,
    delay: number = 500,
  ): (...args: any[]) => void {
    let timer: NodeJS.Timeout | null = null
    let immediate = true

    return (...args: any[]) => {
      if (timer) {
        clearTimeout(timer)
      }

      if (immediate) {
        fn(...args)
        immediate = false
      }

      timer = setTimeout(() => {
        immediate = true
      }, delay)
    }
  }
}

export const { getLanguage, sleep, DeepDeepSleep, getRandString, clickDebounce } = Utils
