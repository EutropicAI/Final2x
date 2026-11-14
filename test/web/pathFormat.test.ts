import PathFormat from '@renderer/utils/pathFormat'
import { describe, expect, it } from 'vitest'

describe('pathFormat', () => {
  it('test_unix', () => {
    const pathFormat = new PathFormat()
    pathFormat.setRootPath('/Users/test/Downloads/unix')
    const check: Array<string> = [
      pathFormat.getRootPath(),
      pathFormat.getNewPath('/unix/test.txt'),
    ]
    expect(check).toStrictEqual(['/Users/test/Downloads', '/Users/test/Downloads/unix/test.txt'])
  })

  it('test_win', () => {
    const pathFormat = new PathFormat()
    pathFormat.setRootPath('C:\\Users\\test\\Downloads\\win')
    const check: Array<string> = [
      pathFormat.getRootPath(),
      pathFormat.getNewPath('/win/test.txt'),
    ]
    expect(check).toStrictEqual([
      'C:\\Users\\test\\Downloads',
      'C:\\Users\\test\\Downloads\\win\\test.txt',
    ])
  })

  it('check_path', () => {
    const check: Array<boolean> = [
      PathFormat.checkPath('/Users/test/Downloads/unix'),
      PathFormat.checkPath('C:\\Users\\test\\Downloads\\win'),
      PathFormat.checkPath('C:Users/test/Downloads/unix/test.txt'),
      PathFormat.checkPath('Users/test/Downloads/unix/test.txt'),
    ]
    expect(check).toStrictEqual([true, true, false, false])
  })

  it('get_file_name', () => {
    expect(PathFormat.getFileName('/Users/test/Downloads/unix/114514.txt')).toBe('114514.txt')
    expect(PathFormat.getFileName('C:\\Users\\test\\Downloads\\win\\genshin.png')).toBe(
      'genshin.png',
    )
  })
})
