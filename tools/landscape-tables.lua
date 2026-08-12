-- Keep large report tables readable: their own landscape pages can span as
-- many pages as needed through Pandoc's normal longtable output.
local LARGE_TABLE_ROWS = 12
local WIDE_TABLE_COLUMNS = 6

local function row_count(table)
  local rows = 0
  for _, body in ipairs(table.bodies) do
    rows = rows + #body.body
  end
  return rows
end

local function is_large(table)
  local rows = row_count(table)
  return rows >= LARGE_TABLE_ROWS
    or (#table.colspecs >= WIDE_TABLE_COLUMNS and rows >= 6)
    or (#table.colspecs >= 5 and rows >= 10)
end

local function is_compact(table)
  return #table.colspecs == 2
end

function Pandoc(doc)
  if not FORMAT:match("latex") then
    return nil
  end

  local blocks = {}
  for index, block in ipairs(doc.blocks) do
    local next_block = doc.blocks[index + 1]
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
