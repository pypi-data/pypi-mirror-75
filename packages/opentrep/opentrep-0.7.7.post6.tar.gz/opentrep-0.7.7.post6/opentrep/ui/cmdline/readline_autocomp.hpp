/**
 * readline_autocomp.hpp -- A tiny application which demonstrates how to use 
 * the GNU Readline library.  This application interactively allows users
 * to manipulate files and their modes.
 */
#ifndef __OPENTREP_READLINE_AUTOCOMP_HPP
#define __OPENTREP_READLINE_AUTOCOMP_HPP

// STL
#include <string>
#include <iosfwd>
#include <cstdio>
#include <sys/types.h>
#include <sys/file.h>
#include <sys/stat.h>
#include <sys/errno.h>

#include <readline/readline.h>
#include <readline/history.h>

extern char* getwd();
extern char* xmalloc (size_t);

/* The names of functions that actually do the manipulation. */
int com_list (char*);
int com_view (char*);
int com_rename (char*);
int com_stat (char*);
int com_pwd (char*);
int com_delete (char*);
int com_help (char*);
int com_cd (char*);
int com_quit (char*);

typedef int (*pt2Func) (char*);

/**
 * A structure which contains information on the commands this program
 * can understand.
 */
typedef struct {
  /**
   * User printable name of the function.
   */
  char const* name;

  /**
   * Function to call to do the job.
   */
  pt2Func *func;

  /**
   * Documentation for this function.
   */
  char *doc;
} COMMAND;

COMMAND commands[] = {
  { "cd", (*com_cd)(), "Change to directory DIR" },
  { "delete", com_delete, "Delete FILE" },
  { "help", com_help, "Display this text" },
  { "?", com_help, "Synonym for `help'" },
  { "list", com_list, "List files in DIR" },
  { "ls", com_list, "Synonym for `list'" },
  { "pwd", com_pwd, "Print the current working directory" },
  { "quit", com_quit, "Quit using opentrep" },
  { "rename", com_rename, "Rename FILE to NEWNAME" },
  { "stat", com_stat, "Print out statistics on FILE" },
  { "view", com_view, "View the contents of FILE" },
  { (char*) NULL, (pt2Func) NULL, (char*) NULL }
};

// Forward declarations
char* stripwhite (char* iString);
COMMAND* find_command (char* iString);

/**
 * When non-zero, this global means the user is done using this program.
 */
int done;

/**
 * Duplicate a string
 */
char* dupstr (char* iString) {
  char* r = xmalloc (std::strlen (iString) + 1);
  strcpy (r, iString);
  return r;
}

/**
 * Execute a command line.
 */
int execute_line (char* line) {
  register int i;
  COMMAND* command;
  char* word;

  /* Isolate the command word. */
  i = 0;
  while (line[i] && whitespace (line[i])) {
    i++;
  }
  word = line + i;

  while (line[i] && !whitespace (line[i])) {
    i++;
  }
  
  if (line[i]) {
    line[i++] = '\0';
  }

  command = find_command (word);

  if (!command) {
    std::cerr << word << ": No such command for opentrep." << std::endl;
    return -1;
  }

  /* Get argument to command, if any. */
  while (whitespace (line[i])) {
    i++;
  }

  word = line + i;

  /* Call the function. */
  return (*(command->func)) (word);
}

/**
 * Look up NAME as the name of a command, and return a pointer to that
 * command.  Return a NULL pointer if NAME isn't a command name.
 */
COMMAND* find_command (char* name) {
  register int i;

  for (i = 0; commands[i].name; i++) {
    if (strcmp (name, commands[i].name) == 0) {
      return (&commands[i]);
    }
  }

  return (COMMAND*) NULL;
}

/**
 * Strip whitespace from the start and end of STRING.
 * Return a pointer into STRING.
 */
char* stripwhite (char* string) {
  register char *s, *t;

  for (s = string; whitespace (*s); s++) {
  }
    
  if (*s == 0) {
    return s;
  }

  t = s + strlen (s) - 1;
  while (t > s && whitespace (*t)) {
    t--;
  }
  *++t = '\0';

  return s;
}

/* **************************************************************** */
/*                                                                  */
/*                  Interface to Readline Completion                */
/*                                                                  */
/* **************************************************************** */

char* command_generator (char* text, int state);
char** fileman_completion (char* text, int start, int end);

/**
 * Tell the GNU Readline library how to complete.  We want to try to complete
 * on command names if this is the first word in the line, or on filenames
 * if not.
 */
void initialize_readline() {
  /* Allow conditional parsing of the ~/.inputrc file. */
  rl_readline_name = "opentrep";

  /* Tell the completer that we want a crack first. */
  rl_attempted_completion_function = (rl_completion_func_t*) fileman_completion;
}

/**
 * Attempt to complete on the contents of TEXT.  START and END bound the
 * region of rl_line_buffer that contains the word to complete.  TEXT is
 * the word to complete.  We can use the entire contents of rl_line_buffer
 * in case we want to do some simple parsing.  Return the array of matches,
 * or NULL if there aren't any.
 */
char** fileman_completion (char* text, int start, int end) {
  char **matches;

  matches = (char**) NULL;

  /**
   * If this word is at the start of the line, then it is a command
   * to complete.  Otherwise it is the name of a file in the current
   * directory.
   */
  if (start == 0) {
    matches = completion_matches (text, command_generator);
  }

  return matches;
}

/**
 * Generator function for command completion.  STATE lets us know whether
 * to start from scratch; without any state (i.e. STATE == 0), then we
 * start at the top of the list.
 */
char* command_generator (char* text, int state) {
  static int list_index, len;
  char* name;

  /**
   * If this is a new word to complete, initialize now.  This includes
   * saving the length of TEXT for efficiency, and initializing the index
   * variable to 0.
   */
  if (!state) {
    list_index = 0;
    len = strlen (text);
  }

  /* Return the next name which partially matches from the command list. */
  while (name = commands[list_index].name) {
    ++list_index;

    if (strncmp (name, text, len) == 0) {
      return dupstr (name);
    }
  }

  /* If no names matched, then return NULL. */
  return (char*) NULL;
}

/* **************************************************************** */
/*                                                                  */
/*                       opentrep Commands                            */
/*                                                                  */
/* **************************************************************** */

/**
 * String to pass to system().  This is for the LIST, VIEW and RENAME
 * commands.
 */
static char syscom[1024];

/**
 * List the file(s) named in arg.
 */
void com_list (char* arg) {
  if (!arg) {
    arg = "";
  }

  std::ostringstream oStr;
  oStr << "ls -FClg " << arg;
  return system (oStr.c_str());
}

int com_view (char* arg) {
  if (!valid_argument ("view", arg)) {
    return 1;
  }

  std::ostringstream oStr;
  oStr << "more " << arg;
  return system (syscom);
}

int com_rename (char* arg) {
  too_dangerous ("rename");
  return 1;
}

int com_stat (char* arg) {
  struct stat finfo;

  if (!valid_argument ("stat", arg)) {
    return 1;
  }

  if (stat (arg, &finfo) == -1) {
    perror (arg);
    return 1;
  }

  std::cout << "Statistics for `" << arg << "':" << std::endl;

  const std::string lPluralEnd1 = (finfo.st_nlink == 1) ? "" : "s";
  const std::string lPluralEnd2 = (finfo.st_size == 1) ? "" : "s";
  std::cout << arg << " has "
            << finfo.st_nlink << " link" << lPluralEnd1 << ", and is "
            << finfo.st_size << " byte" << lPluralEnd2 << " in length."
            << std::endl;
  std::cout << " Inode Last Change at: " << ctime (&finfo.st_ctime) << std::endl;
  std::cout << " Last access at: " << ctime (&finfo.st_atime) << std::endl;
  std::cout << " Last modified at: " << ctime (&finfo.st_mtime) << std::endl;
  return 0;
}

int com_delete (char* arg) {
  too_dangerous ("delete");
  return 1;
}

/**
 * Print out help for ARG, or for all of the commands if ARG is
 * not present.
 */
int com_help (char* arg) {
  register int i;
  int printed = 0;

  for (i = 0; commands[i].name; i++) {
    if (!*arg || (strcmp (arg, commands[i].name) == 0)) {
      printf ("%s\t\t%s.\n", commands[i].name, commands[i].doc);
      printed++;
    }
  }

  if (!printed) {
    printf ("No commands match `%s'.  Possibilties are:\n", arg);

    for (i = 0; commands[i].name; i++) {
      /* Print in six columns. */
      if (printed == 6) {
        printed = 0;
        printf ("\n");
      }

      printf ("%s\t", commands[i].name);
      printed++;
    }

    if (printed)
      printf ("\n");
  }
  return 0;
}

/* Change to the directory ARG. */
int com_cd (char* arg) {
  if (chdir (arg) == -1) {
    perror (arg);
    return 1;
  }

  com_pwd ("");
  return 0;
}

/* Print out the current working directory. */
int com_pwd (char* ignore) {
  char dir[1024], *s;

  s = getwd (dir);
  if (s == 0) {
    printf ("Error getting pwd: %s\n", dir);
    return 1;
  }

  printf ("Current directory is %s\n", dir);
  return 0;
}

/* The user wishes to quit using this program.  Just set DONE non-zero. */
int com_quit (char* arg) {
  done = 1;
  return 0;
}

/* Function which tells you that you can't do this. */
void too_dangerous (char* caller) {
  fprintf (stderr,
           "%s: Too dangerous for me to distribute.  Write it yourself.\n",
           caller);
}

/* Return non-zero if ARG is a valid argument for CALLER, else print
 *    an error message and return zero. */
int valid_argument (char* caller, char* arg) {
  if (!arg || !*arg) {
    fprintf (stderr, "%s: Argument required.\n", caller);
    return 0;
  }

  return 1;
}

#endif // _OPENTREP_READLINE_AUTOCOMP_HPP
