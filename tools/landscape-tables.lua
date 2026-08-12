-- Keep large report tables readable: their own landscape pages can span as
-- many pages as needed through Pandoc's normal longtable output.
local LARGE_TABLE_ROWS = 12

function Table(table)
  if not FORMAT:match("latex") then
    return nil
  end

  local rows = 0
  for _, body in ipairs(table.bodies) do
    rows = rows + #body.body
  end
  if rows < LARGE_TABLE_ROWS then
    return nil
  end

  return {
    pandoc.RawBlock("latex", "\\clearpage\\begin{landscape}\\small"),
    table,
    pandoc.RawBlock("latex", "\\end{landscape}\\clearpage"),
  }
end
