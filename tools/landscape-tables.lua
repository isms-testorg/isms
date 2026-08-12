-- Keep large report tables readable: their own landscape pages can span as
-- many pages as needed through Pandoc's normal longtable output.
local LARGE_TABLE_ROWS = 12
local WIDE_TABLE_COLUMNS = 6
local WORD_BREAK_LENGTH = 14

local function row_count(table)
  local rows = 0
  for _, body in ipairs(table.bodies) do
    rows = rows + #body.body
  end
  return rows
end

local function is_large(table)
  local rows = row_count(table)
  return (#table.colspecs >= 3 and rows >= LARGE_TABLE_ROWS)
    or (#table.colspecs >= WIDE_TABLE_COLUMNS and rows >= 6)
    or (#table.colspecs >= 5 and rows >= 10)
end

local function is_compact(table)
  return #table.colspecs == 2
end

local function wrap_columns(tbl)
  local columns = #tbl.colspecs
  if columns < 3 then
    return tbl
  end
  for column = 1, columns do
    tbl.colspecs[column][2] = 1 / columns
  end
  return tbl:walk({
    Str = function(word)
      if utf8.len(word.text) <= WORD_BREAK_LENGTH or word.text:match("[/%._%-@]") then
        return nil
      end
      local parts, start, length = {}, 1, 0
      for position in utf8.codes(word.text) do
        length = length + 1
        if length == WORD_BREAK_LENGTH then
          local next_position = utf8.offset(word.text, 2, position)
          if next_position then
            table.insert(parts, pandoc.Str(word.text:sub(start, next_position - 1)))
            table.insert(parts, pandoc.RawInline("latex", "\\allowbreak{}"))
            start, length = next_position, 0
          end
        end
      end
      table.insert(parts, pandoc.Str(word.text:sub(start)))
      return parts
    end,
  })
end

function Pandoc(doc)
  if not FORMAT:match("latex") then
    return nil
  end

  local blocks = {}
  for index, block in ipairs(doc.blocks) do
    local next_block = doc.blocks[index + 1]
    if block.t == "Table" then
      -- Markdown defaults to natural-width LaTeX columns. That lets long
      -- German text run into its neighbour instead of wrapping.
      block = wrap_columns(block)
    end
    if block.t == "Header" and next_block and next_block.t == "Table"
      and is_compact(next_block) and row_count(next_block) <= 8 then
      -- Small generated records fit on one page. Reserve their actual height
      -- so longtable cannot start the record and move its final rows alone.
      table.insert(blocks, pandoc.RawBlock("latex", "\\Needspace{16\\baselineskip}"))
      table.insert(blocks, block)
    elseif block.t == "Table" and is_large(block) then
      -- Keep a table's label with its landscape table instead of leaving it
      -- alone on the preceding portrait page.
      local heading = blocks[#blocks]
      if heading and heading.t == "Header" then
        table.remove(blocks)
      end
      table.insert(blocks, pandoc.RawBlock("latex", "\\clearpage\\begin{landscape}\\small"))
      if heading and heading.t == "Header" then
        table.insert(blocks, heading)
      end
      table.insert(blocks, block)
      table.insert(blocks, pandoc.RawBlock(
        "latex", "\\end{landscape}\\clearpage\\pdfpacklandscapefalse\\pagestyle{fancy}"))
    elseif block.t == "Table" and is_compact(block) then
      -- Record-detail tables need less vertical padding than wide indexes. The
      -- former otherwise split across pages despite fitting when laid out as a
      -- compact key/value record.
      table.insert(blocks, pandoc.RawBlock("latex", "\\pdfpackcompacttabletrue"))
      table.insert(blocks, block)
      table.insert(blocks, pandoc.RawBlock("latex", "\\pdfpackcompacttablefalse"))
    else
      table.insert(blocks, block)
    end
  end
  doc.blocks = blocks
  return doc
end
