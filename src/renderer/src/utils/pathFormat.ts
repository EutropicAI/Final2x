class PathFormat {
  private rootpath: string

  constructor() {
    this.rootpath = ''
  }

  /**
   * @description 设置本次上传的根目录
   */
  setRootPath(path: string): void {
    const segments = path.split(/[/\\]/)
    if (segments.length > 1) {
      segments.pop()
      this.rootpath = segments.join(path.startsWith('/')
        ? '/'
        : '\\')
    }
  }

  /**
   * @description 返回本次上传的根目录
   */
  getRootPath(): string {
    return this.rootpath
  }

  /**
   * @description 相对于本次上传的根目录，返回拼接后的真实路径
   */
  getNewPath(path: string): string {
    const segments = path.split(/[/\\]/)
    return this.rootpath + segments.join(this.rootpath.startsWith('/')
      ? '/'
      : '\\')
  }

  /**
   * @description 检查路径格式是否正确
   */
  static checkPath(path: string): boolean {
    return path.startsWith('/') || path.includes('\\')
  }

  /**
   * @description 返回文件名
   */
  static getFileName(path: string): string {
    const segments = path.split(/[/\\]/)
    return segments[segments.length - 1]
  }
}

export default PathFormat
