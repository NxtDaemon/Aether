async def $FUNC_NAME(PARAMS,ctx):
  '$DOCSTRING'
  name = "$NAME"
  try:
    if $VAL == $COND:
      logger.info("$MESSAGE")
      await ctx.send("$USER_MESSAGE")
      return(1)
  except(Exception) as Exc:
      logger.error(f"Uncaught Exception in Module : `{name}`, Error : `{Exc}`")
  else:
    return(0)