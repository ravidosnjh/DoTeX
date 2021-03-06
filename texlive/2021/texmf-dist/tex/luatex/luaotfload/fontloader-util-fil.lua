if not modules then modules = { } end modules ['util-fil'] = {
    version   = 1.001,
    optimize  = true,
    comment   = "companion to luat-lib.mkiv",
    author    = "Hans Hagen, PRAGMA-ADE, Hasselt NL",
    copyright = "PRAGMA ADE / ConTeXt Development Team",
    license   = "see context related readme files"
}

local tonumber = tonumber
local byte = string.byte
local char = string.char

-- Here are a few helpers (the starting point were old ones I used for parsing
-- flac files). In Lua 5.3 we can probably do this better. Some code will move
-- here.

-- We could comment those that are in fio and sio.

utilities       = utilities or { }
local files     = { }
utilities.files = files

-- we could have a gc method that closes but files auto close anyway

local zerobased = { }

function files.open(filename,zb)
    local f = io.open(filename,"rb")
    if f then
        zerobased[f] = zb or false
    end
    return f
end

function files.close(f)
    zerobased[f] = nil
    f:close()
end

function files.size(f)
    local current = f:seek()
    local size = f:seek("end")
    f:seek("set",current)
    return size
end

files.getsize = files.size

function files.setposition(f,n)
    if zerobased[f] then
        f:seek("set",n)
    else
        f:seek("set",n - 1)
    end
end

function files.getposition(f)
    if zerobased[f] then
        return f:seek()
    else
        return f:seek() + 1
    end
end

function files.look(f,n,chars)
    local p = f:seek()
    local s = f:read(n)
    f:seek("set",p)
    if chars then
        return s
    else
        return byte(s,1,#s)
    end
end

function files.skip(f,n)
    if n == 1 then
        f:read(n)
    else
        f:seek("set",f:seek()+n)
    end
end

function files.readbyte(f)
    return byte(f:read(1))
end

function files.readbytes(f,n)
    return byte(f:read(n),1,n)
end

function files.readbytetable(f,n)
 -- return { byte(f:read(n),1,n) }
    local s = f:read(n or 1)
    return { byte(s,1,#s) } -- best use the real length
end

function files.readchar(f)
    return f:read(1)
end

function files.readstring(f,n)
    return f:read(n or 1)
end

function files.readinteger1(f)  -- one byte
    local n = byte(f:read(1))
    if n >= 0x80 then
        return n - 0x100
    else
        return n
    end
end

files.readcardinal1  = files.readbyte  -- one byte
files.readcardinal   = files.readcardinal1
files.readinteger    = files.readinteger1
files.readsignedbyte = files.readinteger1

function files.readcardinal2(f)
    local a, b = byte(f:read(2),1,2)
    return 0x100 * a + b
end

function files.readcardinal2le(f)
    local b, a = byte(f:read(2),1,2)
    return 0x100 * a + b
end

function files.readinteger2(f)
    local a, b = byte(f:read(2),1,2)
    if a >= 0x80 then
        return 0x100 * a + b - 0x10000
    else
        return 0x100 * a + b
    end
end

function files.readinteger2le(f)
    local b, a = byte(f:read(2),1,2)
    if a >= 0x80 then
        return 0x100 * a + b - 0x10000
    else
        return 0x100 * a + b
    end
end

function files.readcardinal3(f)
    local a, b, c = byte(f:read(3),1,3)
    return 0x10000 * a + 0x100 * b + c
end

function files.readcardinal3le(f)
    local c, b, a = byte(f:read(3),1,3)
    return 0x10000 * a + 0x100 * b + c
end

function files.readinteger3(f)
    local a, b, c = byte(f:read(3),1,3)
    if a >= 0x80 then
        return 0x10000 * a + 0x100 * b + c - 0x1000000
    else
        return 0x10000 * a + 0x100 * b + c
    end
end

function files.readinteger3le(f)
    local c, b, a = byte(f:read(3),1,3)
    if a >= 0x80 then
        return 0x10000 * a + 0x100 * b + c - 0x1000000
    else
        return 0x10000 * a + 0x100 * b + c
    end
end

function files.readcardinal4(f)
    local a, b, c, d = byte(f:read(4),1,4)
    return 0x1000000 * a + 0x10000 * b + 0x100 * c + d
end

function files.readcardinal4le(f)
    local d, c, b, a = byte(f:read(4),1,4)
    return 0x1000000 * a + 0x10000 * b + 0x100 * c + d
end

function files.readinteger4(f)
    local a, b, c, d = byte(f:read(4),1,4)
    if a >= 0x80 then
        return 0x1000000 * a + 0x10000 * b + 0x100 * c + d - 0x100000000
    else
        return 0x1000000 * a + 0x10000 * b + 0x100 * c + d
    end
end

function files.readinteger4le(f)
    local d, c, b, a = byte(f:read(4),1,4)
    if a >= 0x80 then
        return 0x1000000 * a + 0x10000 * b + 0x100 * c + d - 0x100000000
    else
        return 0x1000000 * a + 0x10000 * b + 0x100 * c + d
    end
end

function files.readfixed2(f)
    local n1, n2 = byte(f:read(2),1,2)
    if n1 >= 0x80 then
        n1 = n1 - 0x100
    end
    return n1 + n2/0xFF
end

-- (real) (n>>16) + ((n&0xffff)/65536.0)) but no cast in lua (we could use unpack)

function files.readfixed4(f)
    local a, b, c, d = byte(f:read(4),1,4)
    local n1 = 0x100 * a + b
    local n2 = 0x100 * c + d
    if n1 >= 0x8000 then
        n1 = n1 - 0x10000
    end
    return n1 + n2/0xFFFF
end

-- (real) ((n<<16)>>(16+14)) + ((n&0x3fff)/16384.0))

if bit32 then

    local extract = bit32.extract
    local band    = bit32.band

    function files.read2dot14(f)
        local a, b = byte(f:read(2),1,2)
        if a >= 0x80 then
            local n = -(0x100 * a + b)
            return - (extract(n,14,2) + (band(n,0x3FFF) / 16384.0))
        else
            local n =   0x100 * a + b
            return   (extract(n,14,2) + (band(n,0x3FFF) / 16384.0))
        end
    end

end

function files.skipshort(f,n)
    f:read(2*(n or 1))
end

function files.skiplong(f,n)
    f:read(4*(n or 1))
end

-- writers (kind of slow)

if bit32 then

    local rshift = bit32.rshift

    function files.writecardinal2(f,n)
        local a = char(n % 256)
        n = rshift(n,8)
        local b = char(n % 256)
        f:write(b,a)
    end

    function files.writecardinal4(f,n)
        local a = char(n % 256)
        n = rshift(n,8)
        local b = char(n % 256)
        n = rshift(n,8)
        local c = char(n % 256)
        n = rshift(n,8)
        local d = char(n % 256)
        f:write(d,c,b,a)
    end

    function files.writecardinal2le(f,n)
        local a = char(n % 256)
        n = rshift(n,8)
        local b = char(n % 256)
        f:write(a,b)
    end

    function files.writecardinal4le(f,n)
        local a = char(n % 256)
        n = rshift(n,8)
        local b = char(n % 256)
        n = rshift(n,8)
        local c = char(n % 256)
        n = rshift(n,8)
        local d = char(n % 256)
        f:write(a,b,c,d)
    end

else

    local floor = math.floor

    function files.writecardinal2(f,n)
        local a = char(n % 256)
        n = floor(n/256)
        local b = char(n % 256)
        f:write(b,a)
    end

    function files.writecardinal4(f,n)
        local a = char(n % 256)
        n = floor(n/256)
        local b = char(n % 256)
        n = floor(n/256)
        local c = char(n % 256)
        n = floor(n/256)
        local d = char(n % 256)
        f:write(d,c,b,a)
    end

    function files.writecardinal2le(f,n)
        local a = char(n % 256)
        n = floor(n/256)
        local b = char(n % 256)
        f:write(a,b)
    end

    function files.writecardinal4le(f,n)
        local a = char(n % 256)
        n = floor(n/256)
        local b = char(n % 256)
        n = floor(n/256)
        local c = char(n % 256)
        n = floor(n/256)
        local d = char(n % 256)
        f:write(a,b,c,d)
    end

end

function files.writestring(f,s)
    f:write(char(byte(s,1,#s)))
end

function files.writebyte(f,b)
    f:write(char(b))
end

if fio and fio.readcardinal1 then

    files.readcardinal1   = fio.readcardinal1
    files.readcardinal2   = fio.readcardinal2
    files.readcardinal3   = fio.readcardinal3
    files.readcardinal4   = fio.readcardinal4

    files.readcardinal1le = fio.readcardinal1le or files.readcardinal1le
    files.readcardinal2le = fio.readcardinal2le or files.readcardinal2le
    files.readcardinal3le = fio.readcardinal3le or files.readcardinal3le
    files.readcardinal4le = fio.readcardinal4le or files.readcardinal4le

    files.readinteger1    = fio.readinteger1
    files.readinteger2    = fio.readinteger2
    files.readinteger3    = fio.readinteger3
    files.readinteger4    = fio.readinteger4

    files.readinteger1le  = fio.readinteger1le or files.readinteger1le
    files.readinteger2le  = fio.readinteger2le or files.readinteger2le
    files.readinteger3le  = fio.readinteger3le or files.readinteger3le
    files.readinteger4le  = fio.readinteger4le or files.readinteger4le

    files.readfixed2      = fio.readfixed2
    files.readfixed4      = fio.readfixed4
    files.read2dot14      = fio.read2dot14
    files.setposition     = fio.setposition
    files.getposition     = fio.getposition

    files.readbyte        = files.readcardinal1
    files.readsignedbyte  = files.readinteger1
    files.readcardinal    = files.readcardinal1
    files.readinteger     = files.readinteger1

    local skipposition    = fio.skipposition
    files.skipposition    = skipposition

    files.readbytes       = fio.readbytes
    files.readbytetable   = fio.readbytetable

    function files.skipshort(f,n)
        skipposition(f,2*(n or 1))
    end

    function files.skiplong(f,n)
        skipposition(f,4*(n or 1))
    end

end

if fio and fio.writecardinal1 then

    files.writecardinal1   = fio.writecardinal1
    files.writecardinal2   = fio.writecardinal2
    files.writecardinal3   = fio.writecardinal3
    files.writecardinal4   = fio.writecardinal4

    files.writecardinal1le = fio.writecardinal1le
    files.writecardinal2le = fio.writecardinal2le
    files.writecardinal3le = fio.writecardinal3le
    files.writecardinal4le = fio.writecardinal4le

    files.writeinteger1    = fio.writeinteger1 or fio.writecardinal1
    files.writeinteger2    = fio.writeinteger2 or fio.writecardinal2
    files.writeinteger3    = fio.writeinteger3 or fio.writecardinal3
    files.writeinteger4    = fio.writeinteger4 or fio.writecardinal4

    files.writeinteger1le  = files.writeinteger1le or fio.writecardinal1le
    files.writeinteger2le  = files.writeinteger2le or fio.writecardinal2le
    files.writeinteger3le  = files.writeinteger3le or fio.writecardinal3le
    files.writeinteger4le  = files.writeinteger4le or fio.writecardinal4le

end

if fio and fio.readcardinaltable then

    files.readcardinaltable = fio.readcardinaltable
    files.readintegertable  = fio.readintegertable

else

    local readcardinal1 = files.readcardinal1
    local readcardinal2 = files.readcardinal2
    local readcardinal3 = files.readcardinal3
    local readcardinal4 = files.readcardinal4

    function files.readcardinaltable(f,n,b)
        local t = { }
            if b == 1 then for i=1,n do t[i] = readcardinal1(f) end
        elseif b == 2 then for i=1,n do t[i] = readcardinal2(f) end
        elseif b == 3 then for i=1,n do t[i] = readcardinal3(f) end
        elseif b == 4 then for i=1,n do t[i] = readcardinal4(f) end end
        return t
    end

    local readinteger1 = files.readinteger1
    local readinteger2 = files.readinteger2
    local readinteger3 = files.readinteger3
    local readinteger4 = files.readinteger4

    function files.readintegertable(f,n,b)
        local t = { }
            if b == 1 then for i=1,n do t[i] = readinteger1(f) end
        elseif b == 2 then for i=1,n do t[i] = readinteger2(f) end
        elseif b == 3 then for i=1,n do t[i] = readinteger3(f) end
        elseif b == 4 then for i=1,n do t[i] = readinteger4(f) end end
        return t
    end

end
