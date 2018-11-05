package com.sparkProject

import org.apache.spark.SparkConf
import org.apache.spark.ml.Pipeline
import org.apache.spark.ml.classification.LogisticRegression
import org.apache.spark.ml.feature._
import org.apache.spark.sql.SparkSession
import org.apache.spark.ml.tuning.TrainValidationSplit
import org.apache.spark.ml.tuning.{CrossValidator, ParamGridBuilder}
import org.apache.spark.ml.evaluation.MulticlassClassificationEvaluator

object Trainer {

  def main(args: Array[String]): Unit = {

    val conf = new SparkConf().setAll(Map(
      "spark.scheduler.mode" -> "FIFO",
      "spark.speculation" -> "false",
      "spark.reducer.maxSizeInFlight" -> "48m",
      "spark.serializer" -> "org.apache.spark.serializer.KryoSerializer",
      "spark.kryoserializer.buffer.max" -> "1g",
      "spark.shuffle.file.buffer" -> "32k",
      "spark.default.parallelism" -> "12",
      "spark.sql.shuffle.partitions" -> "12",
      "spark.driver.maxResultSize" -> "2g"
    ))

    val spark = SparkSession
      .builder
      .config(conf)
      .appName("TP_spark")
      .getOrCreate()


    /*******************************************************************************
      *
      *       TP 3
      *
      *       - lire le fichier sauvegarder précédemment
      *       - construire les Stages du pipeline, puis les assembler
      *       - trouver les meilleurs hyperparamètres pour l'entraînement du pipeline avec une grid-search
      *       - Sauvegarder le pipeline entraîné
      *
      *       if problems with unimported modules => sbt plugins update
      *
      ********************************************************************************/
    println("hello world ! from Trainer")
    val df = spark.read.parquet("./prepared_trainingset/*")
    // df.show()

    println(df.count(), df.columns.length)
    // println(df.columns.toString())
    val tokenizer = new RegexTokenizer()
     .setPattern("\\W+")
     .setGaps(true)
     .setInputCol("text")
     .setOutputCol("tokens")

    val remover = new StopWordsRemover().setInputCol("tokens")
     .setOutputCol("sw_rm")

    val cvModel: CountVectorizer = new CountVectorizer()
     .setInputCol("sw_rm")
     .setOutputCol("count_vectorized")

    val idf = new IDF().setInputCol("count_vectorized").setOutputCol("tfidf")

    //val rm = remover.transform(tokenizer.transform(df))//.select("sw_rm").show()
    //val cv = cvModel.fit(rm).transform(rm).select("count_vectorized")
    //idf.fit(cv).transform(cv).select("tfidf").show()
//
    val indexer1 = new StringIndexer().setInputCol("country2").setOutputCol("country_indexed")
    val indexer2 = new StringIndexer().setInputCol("currency2").setOutputCol("currency_indexed")

    val encoder1 = new OneHotEncoder().setInputCol("country_indexed").setOutputCol("country_encoded")
    val encoder2 = new OneHotEncoder().setInputCol("currency_indexed").setOutputCol("currency_encoded")
//
    val assembler = new VectorAssembler()
     .setInputCols(Array("tfidf", "days_campaign", "hours_prepa", "goal", "country_indexed", "currency_indexed"))
     .setOutputCol("features")
//
    val lr = new LogisticRegression()
     .setElasticNetParam(0.0)
     .setFitIntercept(true)
     .setFeaturesCol("features")
     .setLabelCol("final_status")
     .setStandardization(true)
     .setPredictionCol("predictions")
     .setRawPredictionCol("raw_predictions")
     .setThresholds(Array(0.7, 0.3))
     .setTol(1.0e-6)
     .setMaxIter(300)

    val pipeline = new Pipeline()
     .setStages(Array(tokenizer, remover, cvModel, idf, indexer1, indexer2, encoder1, encoder2,assembler, lr))
//    pipeline.fit(df)
    //pipeline.write.overwrite().save("./pipeline")
    val Array(training, test) = df.randomSplit(Array[Double](0.9, 0.1))

    val lr_param = (-8 to -2 by 2).map(x => Math.pow(10,x)).toArray
    val cvModel_param = (55.0 to 95.0 by 20).toArray

    val paramGrid = new ParamGridBuilder()
  .addGrid(lr.regParam, lr_param)
  .addGrid(cvModel.minDF, cvModel_param)
  .build()

  val evaluator = new MulticlassClassificationEvaluator()
    .setLabelCol("final_status")
    .setPredictionCol("predictions")
    .setMetricName("f1")

    val trainValidationSplit = new TrainValidationSplit()
  .setEstimator(pipeline)
  .setEvaluator(evaluator)
  .setEstimatorParamMaps(paramGrid)
  // 70% of the data will be used for training and the remaining 30% for validation.
  .setTrainRatio(0.7)

  val model = trainValidationSplit.fit(training)

  val df_WithPredictions = model.transform(test)
                                .select("features", "final_status", "predictions")

  val f1_score = evaluator.evaluate(df_WithPredictions)

  println("f1-score on test set: " + f1_score)

  df_WithPredictions.groupBy("final_status", "predictions").count.show()
  }
}
