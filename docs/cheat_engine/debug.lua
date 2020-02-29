-- 调试KERNELBASE.WriteProcessMemory
function debugger_onBreakpoint()
    local data = readBytes(R8, R9, true)
    local hexdata = {}
    for k, v in ipairs(data) do
        hexdata[k] = string.format('%02X', v)
    end
    local buffer = string.format("'%s'", table.concat(hexdata, ' '))
    local result = string.format('WriteProcessMemory(address=0x%08X, buffer=%s, size=%d)', RDX, buffer, R9)
    print(result)
    return 1
end

debug_setBreakpoint(getAddress('KERNELBASE.WriteProcessMemory') + 0x13)


function findBytes(data)
    local result = AOBScan(data, '+X-C-W')
    for i=0, result.Count - 1 do
        if string.find(result[i], '7FF') == 1 then
            print(result[i], data)
        end
    end
end

print(string.format("base=0x%08X", getAddress('re2.exe')))


-- 写入文件
print(writeRegionToFile('F:/Temp/1.txt', 0x0087C9E6, 1024 * 20))
