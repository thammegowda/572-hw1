package edu.usc.cs.ir.fall15.grp36;

import com.google.gson.JsonElement;
import org.apache.commons.io.FileUtils;
import org.apache.commons.io.IOUtils;
import org.apache.commons.io.filefilter.TrueFileFilter;
import org.apache.tika.Tika;
import org.apache.tika.metadata.Metadata;
import org.apache.tika.metadata.serialization.JsonMetadataSerializer;
import org.kohsuke.args4j.CmdLineException;
import org.kohsuke.args4j.CmdLineParser;
import org.kohsuke.args4j.Option;

import java.io.*;
import java.util.Collection;

/**
 * Dumps metadata of files using tika
 * @author ThammeGowda N and members from Team-36
 *
 */
public class MetadataDumper {

    private Tika tika = new Tika();
    private JsonMetadataSerializer serializer = new JsonMetadataSerializer();
    private boolean verbose = true;

    private long dumper(File inputDir, OutputStream outputStream) throws IOException {

        System.out.println("Finding children");
        Collection<File> files = FileUtils.listFiles(inputDir, TrueFileFilter.INSTANCE, TrueFileFilter.INSTANCE);
        System.out.println("Found " + files.size() + " child files");
        BufferedWriter writer = new BufferedWriter(new OutputStreamWriter(outputStream));
        long count = 0;
        long lastt = System.currentTimeMillis();
        for (File file : files) {
            if (!file.isFile()) {
                System.out.println("Not a file :" + file.getAbsolutePath());
                continue;
            }
            Metadata md = new Metadata();
            tika.parse(new FileInputStream(file), md);
            md.add("__path__", file.getAbsolutePath());

            JsonElement element = serializer.serialize(md, null, null);
            writer.write(file.getAbsolutePath());
            writer.write("\t:\t");
            writer.write(element.toString());
            writer.write("\n");
            count++;
            if (verbose && System.currentTimeMillis() - lastt > 2000){
                System.out.println("Count :" + count);
                lastt = System.currentTimeMillis();
            }
        }
        IOUtils.closeQuietly(writer);
        return count;
    }


    private static class CliArgs{
        @Option(name = "-inputDir", usage = "Path to input directory. This is a root directory which contains files" +
                " whose metadata needs to be dumped", required = true)
        private String rootDir;
        @Option(name = "-output", usage = "Path to output file (a json line file will be created here)", required = true)
        private String outputFile;
    }

    public static void main(String[] argv) throws CmdLineException, IOException {
        CliArgs args = new CliArgs();
        CmdLineParser parser = new CmdLineParser(args);
        try {
            parser.parseArgument(argv);
        } catch (CmdLineException e) {
            System.err.println("ERROR:Invalid Args\nUsage:");
            e.getParser().printUsage(System.err);
            throw e;
        }

        MetadataDumper dumper = new MetadataDumper();
        File outputFile = new File(args.outputFile);
        File inputDir = new File(args.rootDir);
        if (outputFile.exists()) {
            throw new IllegalStateException(args.outputFile + " already exists");
        }
        if (!inputDir.exists()) {
            throw new IllegalStateException(args.rootDir + " doesn't exists");
        }

        OutputStream stream = new FileOutputStream(outputFile);
        //dump
        long count = dumper.dumper(inputDir, stream);
        System.out.printf("Found : " + count + " files");
        System.out.println("==Done==");
    }
}
